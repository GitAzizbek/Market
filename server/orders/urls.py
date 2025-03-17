from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')

urlpatterns = [
    path('', include(router.urls)),
    path('cashbox/', CashboxView.as_view(), name='cashbox'),
    path('upload/<int:order_id>', UploadCheck.as_view())
]