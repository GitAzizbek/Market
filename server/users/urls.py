from django.urls import path
from .views import *

urlpatterns = [
    path('login', UserLoginView.as_view()),
    path('update', UserUpdateAPIView.as_view())
]