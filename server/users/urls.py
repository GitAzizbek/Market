from django.urls import path
from .views import *

urlpatterns = [
    path('login', UserLoginView.as_view()),
    path('update', UserUpdateAPIView.as_view()),
    path('profile', ProfileView.as_view())
]