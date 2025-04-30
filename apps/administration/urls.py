from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminImageViewSet, AdminOrderFormsViewSet

router = DefaultRouter()
router.register(r'administration/images', AdminImageViewSet)
router.register(r'administration/order-forms', AdminOrderFormsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]