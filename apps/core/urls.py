from django.urls import path

from apps.core.views import ImageListCreateView, OrderFormListCreateView

urlpatterns = [
    path('images/', ImageListCreateView.as_view(), name='image-list-create'),
    path('order-forms/', OrderFormListCreateView.as_view(), name='orderform-list-create'),

]
