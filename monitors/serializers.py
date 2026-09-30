from rest_framework import serializers

from .models import Monitor


class MonitorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Monitor
        fields = [
            "id",
            "name",
            "url",
            "method",
            "expected_status",
            "timeout",
            "interval",
            "is_active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]