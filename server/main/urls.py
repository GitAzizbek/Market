from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'reviews', ReviewViewSet, basename='reviews')
router.register(r'category', CategoryViewSet, basename='categories')

urlpatterns = [
    path('', include(router.urls)),
    path('announce/', GetAnnounce.as_view())
]
