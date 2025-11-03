from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserRegisterView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,TokenRefreshView
)

router = DefaultRouter() 

urlpatterns =  (
    [
        path('users/register/',UserRegisterView.as_view(),name='register'),
        path('users/login/',TokenObtainPairView.as_view(),name="login"),
        path('users/login/refresh/',TokenRefreshView.as_view(),name="login-refresh"),
         
    ]  + router.urls
)