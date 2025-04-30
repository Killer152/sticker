import logging

from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import IsAdminUser

from .serializers import AdminImageSerializer, AdminOrderFormsSerializer
from ..core.models import Image, OrderForms
from ..core.pagination import CustomPagination

logger = logging.getLogger(__name__)


class AdminImageViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    Admin viewset for Images with list, patch, and delete operations
    """
    queryset = Image.objects.all()
    serializer_class = AdminImageSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['approved', 'upload_date']
    search_fields = ['title', 'original_filename', 'ip_address']
    ordering_fields = ['upload_date', 'id', 'title']
    ordering = ['-upload_date']

    @transaction.atomic
    def perform_destroy(self, instance):
        """
        When deleting an image, also delete the file from storage
        """
        try:
            image_id = instance.id
            image_path = instance.image.path if instance.image else "No file"

            if instance.image:
                instance.image.delete(save=False)

            instance.delete()

            logger.info(f"Admin deleted image ID:{image_id}, Path:{image_path}")

        except Exception as e:
            logger.error(f"Error deleting image ID:{instance.id}: {str(e)}")
            raise


class AdminOrderFormsViewSet(mixins.ListModelMixin,
                             mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin,
                             mixins.DestroyModelMixin,
                             viewsets.GenericViewSet):
    """
    Admin viewset for Order Forms with list, patch, and delete operations
    """
    queryset = OrderForms.objects.all()
    serializer_class = AdminOrderFormsSerializer
    permission_classes = [IsAdminUser]
    pagination_class = CustomPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['contact_method', 'created_at']
    search_fields = ['name', 'phone']
    ordering_fields = ['created_at', 'id', 'name']
    ordering = ['-created_at']

    def perform_destroy(self, instance):
        """
        Log order form deletion
        """
        try:
            order_id = instance.id
            order_name = instance.name

            instance.delete()

            logger.info(f"Admin deleted order form ID:{order_id}, Name:{order_name}")

        except Exception as e:
            logger.error(f"Error deleting order form ID:{instance.id}: {str(e)}")
            raise
