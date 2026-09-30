from datetime import timedelta

from celery import shared_task
from django.utils import timezone

from monitors.models import Monitor
from .models import Incident
from .services import check_monitor
from django.conf import settings
from .email_service import (
    send_incident_started_email,
    send_incident_resolved_email,
)

@shared_task
def check_monitor_task(monitor_id):
    try:
        monitor = Monitor.objects.get(
            id=monitor_id,
            is_active=True
        )
    except Monitor.DoesNotExist:
        return {
            "success": False,
            "message": "Monitor not found or inactive."
        }

    result = check_monitor(monitor)

    monitor.last_checked_at = timezone.now()
    monitor.save(update_fields=["last_checked_at"])

    if result["success"]:
        resolve_incident(monitor)
    else:
        handle_failure(monitor)

    return result


def handle_failure(monitor):
    incident = Incident.objects.filter(
        monitor=monitor,
        is_resolved=False
    ).first()

    if incident:
        incident.failure_count += 1
        incident.save(update_fields=["failure_count"])
        return

    recent_results = monitor.check_results.order_by("-checked_at")[:3]

    if (
        len(recent_results) == 3
        and all(not result.is_success for result in recent_results)
    ):
        incident = Incident.objects.create(
            monitor=monitor,
            failure_count=3
        )

        send_incident_started_email_task.delay(incident.id)

@shared_task
def schedule_monitor_checks():
    now = timezone.now()

    monitors = Monitor.objects.filter(is_active=True)

    scheduled = 0

    for monitor in monitors:
        if (
            monitor.last_checked_at is None
            or now - monitor.last_checked_at
            >= timedelta(minutes=monitor.interval)
        ):
            check_monitor_task.delay(monitor.id)
            scheduled += 1

    return {"scheduled": scheduled}

@shared_task
def send_incident_started_email_task(incident_id):
    try:
        incident = Incident.objects.get(id=incident_id)
    except Incident.DoesNotExist:
        return {
            "success": False,
            "message": "Incident not found."
        }

    send_incident_started_email(incident)

    return {
        "success": True,
        "message": "Incident started email sent."
    }
@shared_task
def send_incident_resolved_email_task(incident_id):
    try:
        incident = Incident.objects.get(id=incident_id)
    except Incident.DoesNotExist:
        return {
            "success": False,
            "message": "Incident not found."
        }

    send_incident_resolved_email(incident)

    return {
        "success": True,
        "message": "Incident resolved email sent."
    }

def resolve_incident(monitor):
    incident = Incident.objects.filter(
        monitor=monitor,
        is_resolved=False
    ).first()

    if incident:
        incident.is_resolved = True
        incident.resolved_at = timezone.now()
        incident.save(
            update_fields=["is_resolved", "resolved_at"]
        )

        send_incident_resolved_email_task.delay(incident.id)