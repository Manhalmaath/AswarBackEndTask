from rest_framework.generics import ListCreateAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

from core.Utilities.permissions import IsAuthenticated
from core.models import Tag
from core.serializers import TagSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class TagViewSet(ListCreateAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Tag.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class SingleTagViewSet(UpdateAPIView, DestroyAPIView):
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        return Tag.objects.filter(created_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
