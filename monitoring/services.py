import time

import requests

from .models import CheckResult


def check_monitor(monitor):
    start_time = time.perf_counter()

    try:
        response = requests.request(
            method=monitor.method,
            url=monitor.url,
            timeout=monitor.timeout,
        )

        response_time = time.perf_counter() - start_time

        is_success = response.status_code == monitor.expected_status

        CheckResult.objects.create(
            monitor=monitor,
            status_code=response.status_code,
            response_time=response_time,
            is_success=is_success,
            error_message=None,
        )

        return {
            "success": is_success,
            "status_code": response.status_code,
            "response_time": response_time,
        }

    except requests.RequestException as error:

        response_time = time.perf_counter() - start_time

        CheckResult.objects.create(
            monitor=monitor,
            status_code=None,
            response_time=response_time,
            is_success=False,
            error_message=str(error),
        )

        return {
            "success": False,
            "status_code": None,
            "response_time": response_time,
            "error": str(error),
        }