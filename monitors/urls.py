from django.urls import path
from .views import (
    MonitorListCreateView,
    MonitorDetailView,
)

urlpatterns = [

    path(
        "",
        MonitorListCreateView.as_view(),
        name="monitor-list-create"
    ),

    path(
        "<int:pk>/",
        MonitorDetailView.as_view(),
        name="monitor-detail"
    ),

]