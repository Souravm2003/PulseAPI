from django.core.mail import EmailMessage
from django.core import mail


from django.core.mail import EmailMessage, get_connection


def send_incident_started_email(incident):
    monitor = incident.monitor

    connection = get_connection(
        backend="django.core.mail.backends.console.EmailBackend"
    )

    email = EmailMessage(
        subject=f"🚨 Incident Started - {monitor.name}",
        body=(
            f"Your monitor '{monitor.name}' is experiencing failures.\n\n"
            f"URL: {monitor.url}\n"
            f"Failure count: {incident.failure_count}\n"
            f"Started at: {incident.started_at}\n"
        ),
        from_email="pulseapi@example.com",
        to=[monitor.user.email],
        connection=connection,
    )

    email.send()

def send_incident_resolved_email(incident):
    monitor = incident.monitor

    connection = get_connection(
        backend="django.core.mail.backends.console.EmailBackend"
    )

    email = EmailMessage(
        subject=f"✅ Incident Resolved - {monitor.name}",
        body=(
            f"Your monitor '{monitor.name}' has recovered.\n\n"
            f"URL: {monitor.url}\n"
            f"Resolved at: {incident.resolved_at}\n"
        ),
        from_email="pulseapi@example.com",
        to=[monitor.user.email],
        connection=connection,
    )

    email.send()