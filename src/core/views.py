"""
Core views for app.
"""
from rest_framework.generics import RetrieveAPIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response


class HealthCheckView(RetrieveAPIView):
    def get_serializer_class(self):
        return None

    def get(self, request, *args, **kwargs):
        """Returns successful response."""
        return Response({"healthy": True})
