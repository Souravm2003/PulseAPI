from django.urls import path
from django.http import JsonResponse
from .views import CheckResultListView, IncidentListView, MonitorAnalyticsView
from .views import dashboard

def health_check(request):
    return JsonResponse({"status": "ok"})


urlpatterns = [
    path("health/", health_check),
    path(
    "monitors/<int:monitor_id>/checks/",
    CheckResultListView.as_view(),
    name="check-results"),
    path(
    "monitors/<int:monitor_id>/incidents/",
    IncidentListView.as_view(),
    name="incident-list"),
    path(
        "monitors/<int:monitor_id>/analytics/",
        MonitorAnalyticsView.as_view(),
        name="monitor-analytics"),
    path("dashboard/", dashboard, name="dashboard"),
]