from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Monitor
from .serializers import MonitorSerializer


class MonitorListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        monitors = Monitor.objects.filter(user=request.user)

        serializer = MonitorSerializer(monitors, many=True)

        return Response(serializer.data)

    def post(self, request):
        serializer = MonitorSerializer(data=request.data)

        if serializer.is_valid():
            monitor = serializer.save(user=request.user)

            return Response(
                MonitorSerializer(monitor).data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class MonitorDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get_monitor(self, request, pk):
        try:
            return Monitor.objects.get(
                id=pk,
                user=request.user
            )
        except Monitor.DoesNotExist:
            return None

    def get(self, request, pk):
        monitor = self.get_monitor(request, pk)

        if not monitor:
            return Response(
                {"detail": "Monitor not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MonitorSerializer(monitor)

        return Response(serializer.data)

    def put(self, request, pk):
        monitor = self.get_monitor(request, pk)

        if not monitor:
            return Response(
                {"detail": "Monitor not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MonitorSerializer(
            monitor,
            data=request.data
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def patch(self, request, pk):
        monitor = self.get_monitor(request, pk)

        if not monitor:
            return Response(
                {"detail": "Monitor not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = MonitorSerializer(
            monitor,
            data=request.data,
            partial=True
        )

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data)

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        monitor = self.get_monitor(request, pk)

        if not monitor:
            return Response(
                {"detail": "Monitor not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        monitor.delete()

        return Response(
            {"message": "Monitor deleted successfully."},
            status=status.HTTP_204_NO_CONTENT
        )