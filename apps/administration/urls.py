from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AdminImageViewSet, AdminOrderFormsViewSet

router = DefaultRouter()
router.register(r'images', AdminImageViewSet)
router.register(r'order-forms', AdminOrderFormsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]