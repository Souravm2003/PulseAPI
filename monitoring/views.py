from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from monitors.models import Monitor
from .serializers import CheckResultSerializer, IncidentSerializer
from .analytics import get_monitor_analytics


class CheckResultListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, monitor_id):
        try:
            monitor = Monitor.objects.get(
                id=monitor_id,
                user=request.user
            )
        except Monitor.DoesNotExist:
            return Response(
                {"detail": "Monitor not found."},
                status=404
            )

        check_results = monitor.check_results.order_by("-checked_at")

        serializer = CheckResultSerializer(
            check_results,
            many=True
        )

        return Response(serializer.data)

class IncidentListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, monitor_id):
        try:
            monitor = Monitor.objects.get(
                id=monitor_id,
                user=request.user
            )
        except Monitor.DoesNotExist:
            return Response(
                {"detail": "Monitor not found."},
                status=404
            )

        incidents = monitor.incidents.order_by("-started_at")

        serializer = IncidentSerializer(
            incidents,
            many=True
        )

        return Response(serializer.data)

class MonitorAnalyticsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, monitor_id):
        try:
            monitor = Monitor.objects.get(
                id=monitor_id,
                user=request.user
            )
        except Monitor.DoesNotExist:
            return Response(
                {"detail": "Monitor not found."},
                status=404
            )

        time_range = request.query_params.get(
            "range",
            "24h"
        )

        try:
            analytics = get_monitor_analytics(
                monitor,
                time_range
            )
        except ValueError as error:
            return Response(
                {"detail": str(error)},
                status=400
            )

        return Response(analytics)

from django.shortcuts import render


def dashboard(request):
    return render(request, "dashboard.html")

def landing(request):
    return render(request, "landing.html")

def login_page(request):
    return render(request, "login.html")


def register_page(request):
    return render(request, "register.html")

def monitor_detail(request, monitor_id):
    return render(
        request,
        "monitor-detail.html",
        {
            "monitor_id": monitor_id
        }
    )
def settings_page(request):
    return render(request, "settings.html")