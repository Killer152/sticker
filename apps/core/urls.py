from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ImageViewSet, OrderFormsViewSet

router = DefaultRouter()
router.register(r'images', ImageViewSet)
router.register(r'order-forms', OrderFormsViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
