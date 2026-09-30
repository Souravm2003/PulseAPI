from datetime import timedelta
from statistics import quantiles

from django.db.models import Avg
from django.utils import timezone


def get_monitor_analytics(monitor, time_range="24h"):

    now = timezone.now()

    # ---------------------------------------------------------
    # TIME RANGE
    # ---------------------------------------------------------

    if time_range == "24h":

        start_time = now - timedelta(hours=24)

    elif time_range == "7d":

        start_time = now - timedelta(days=7)

    elif time_range == "30d":

        start_time = now - timedelta(days=30)

    else:

        raise ValueError("Invalid time range.")


    # ---------------------------------------------------------
    # CHECK RESULTS
    # ---------------------------------------------------------

    check_results = monitor.check_results.filter(
        checked_at__gte=start_time
    )


    total_checks = check_results.count()


    successful_checks = check_results.filter(
        is_success=True
    ).count()


    failed_checks = check_results.filter(
        is_success=False
    ).count()


    # ---------------------------------------------------------
    # UPTIME
    # ---------------------------------------------------------

    if total_checks > 0:

        uptime_percentage = (
            successful_checks /
            total_checks
        ) * 100

    else:

        uptime_percentage = 0


    # ---------------------------------------------------------
    # FAILURE RATE
    # ---------------------------------------------------------

    if total_checks > 0:

        failure_rate_percentage = (
            failed_checks /
            total_checks
        ) * 100

    else:

        failure_rate_percentage = 0


    # ---------------------------------------------------------
    # RESPONSE TIMES
    #
    # Only successful checks are used for response-time
    # statistics.
    # ---------------------------------------------------------

    successful_results = (
        check_results
        .filter(is_success=True)
        .exclude(response_time=None)
    )


    # ---------------------------------------------------------
    # AVERAGE RESPONSE TIME
    # ---------------------------------------------------------

    average_response_time = (
        successful_results
        .aggregate(
            average=Avg("response_time")
        )["average"]
    )


    # ---------------------------------------------------------
    # RESPONSE TIME LIST
    # ---------------------------------------------------------

    response_times = list(
        successful_results
        .values_list(
            "response_time",
            flat=True
        )
    )


    # ---------------------------------------------------------
    # P95 / P99
    # ---------------------------------------------------------

    p95_response_time = None
    p99_response_time = None


    if len(response_times) >= 2:

        percentile_values = quantiles(
            response_times,
            n=100
        )

        p95_response_time = (
            percentile_values[94]
        )

        p99_response_time = (
            percentile_values[98]
        )


    # ---------------------------------------------------------
    # CONVERT SECONDS → MILLISECONDS
    # ---------------------------------------------------------

    average_response_time_ms = (
        average_response_time * 1000
        if average_response_time is not None
        else None
    )


    p95_response_time_ms = (
        p95_response_time * 1000
        if p95_response_time is not None
        else None
    )


    p99_response_time_ms = (
        p99_response_time * 1000
        if p99_response_time is not None
        else None
    )


    # ---------------------------------------------------------
    # ROUND VALUES
    # ---------------------------------------------------------

    uptime_percentage = round(
        uptime_percentage,
        2
    )


    failure_rate_percentage = round(
        failure_rate_percentage,
        2
    )


    if average_response_time_ms is not None:

        average_response_time_ms = round(
            average_response_time_ms,
            2
        )


    if p95_response_time_ms is not None:

        p95_response_time_ms = round(
            p95_response_time_ms,
            2
        )


    if p99_response_time_ms is not None:

        p99_response_time_ms = round(
            p99_response_time_ms,
            2
        )


    # ---------------------------------------------------------
    # RETURN ANALYTICS
    # ---------------------------------------------------------

    return {

        "time_range": time_range,


        # Basic check statistics

        "total_checks": total_checks,

        "successful_checks": successful_checks,

        "failed_checks": failed_checks,


        # Uptime / failure

        "uptime_percentage": uptime_percentage,

        "failure_rate_percentage": failure_rate_percentage,


        # Response time

        "average_response_time_ms":
            average_response_time_ms,

        "p95_response_time_ms":
            p95_response_time_ms,

        "p99_response_time_ms":
            p99_response_time_ms,


        # -----------------------------------------------------
        # Frontend-friendly aliases
        #
        # These match what dashboard/monitor-detail.html
        # expects.
        # -----------------------------------------------------

        "uptime":
            uptime_percentage,

        "failure":
            failure_rate_percentage,

        "avg":
            average_response_time_ms,

        "avg_response_time":
            average_response_time_ms,

        "avg_response_time_ms":
            average_response_time_ms,

        "p95":
            p95_response_time_ms,

        "p99":
            p99_response_time_ms,

    }