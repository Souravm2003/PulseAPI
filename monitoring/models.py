from django.db import models
from monitors.models import Monitor

class CheckResult(models.Model):

    monitor = models.ForeignKey(
        Monitor,
        on_delete=models.CASCADE,
        related_name="check_results"
    )

    status_code = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    response_time = models.FloatField(
        null=True,
        blank=True
    )

    is_success = models.BooleanField(
        default=False
    )

    error_message = models.TextField(
        null=True,
        blank=True
    )

    checked_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.monitor.name} - {self.status_code}"

class Incident(models.Model):
    monitor = models.ForeignKey(
        Monitor,
        on_delete=models.CASCADE,
        related_name="incidents"
    )
    started_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    is_resolved = models.BooleanField(default=False)
    failure_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.monitor.name} - Incident"