from django.urls import path
from authentication import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)

urlpatterns = [
    path('register', views.register, name='register'),
    path('login', TokenObtainPairView.as_view(), name='login'),
    path('refresh', TokenRefreshView.as_view(), name='refresh'),
    path('verify', TokenVerifyView.as_view(), name='verify'),
]
