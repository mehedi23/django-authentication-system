from django.shortcuts import render  
from .serializers import UserRegisterSerializer
from apps.users.services.registration import BaseRegistrationView
from .models import User
# Create your views here.

class UserRegisterView(BaseRegistrationView):
    model = User
    serializer_class = UserRegisterSerializer
    response_keys = ['access',]
    access_keys = ['id', 'username', 'email','is_phone_verify','is_email_verify']