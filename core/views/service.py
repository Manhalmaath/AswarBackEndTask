from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from core.Utilities.permissions import IsAuthenticated
from core.models import Service
from core.serializers import ServiceSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class ServiceViewSet(ListCreateAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Service.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SingleServiceViewSet(UpdateAPIView, DestroyAPIView):
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Service.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
