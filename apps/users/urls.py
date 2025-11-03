from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterView, UserView, ChangePasswordView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,TokenRefreshView
)

router = DefaultRouter() 

urlpatterns =  (
    [
        path('users/me/',UserView.as_view(),name='self-me'),
        path("users/me/change-password/", ChangePasswordView.as_view(), name="change-password"),
        path('users/register/',UserRegisterView.as_view(),name='register'),
        path('users/login/',TokenObtainPairView.as_view(),name="login"),
        path('users/login/refresh/',TokenRefreshView.as_view(),name="login-refresh"),
         
    ]  + router.urls
)