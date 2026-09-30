from rest_framework import serializers
from .models import CheckResult, Incident


class CheckResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckResult
        fields = [
            "id",
            "status_code",
            "response_time",
            "is_success",
            "error_message",
            "checked_at",
        ]
        read_only_fields = [
            "id",
            "status_code",
            "response_time",
            "is_success",
            "error_message",
            "checked_at",
        ]

class IncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incident
        fields = [
            "id",
            "started_at",
            "resolved_at",
            "is_resolved",
            "failure_count",
        ]
        read_only_fields = [
            "id",
            "started_at",
            "resolved_at",
            "is_resolved",
            "failure_count",
        ]