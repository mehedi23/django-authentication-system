from django.shortcuts import render  
from .serializers import UserRegisterSerializer
from apps.users.services.registration import BaseRegistrationView
from .models import User 
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import UserSerializer  # your user serializer
# Create your views here.

class UserRegisterView(BaseRegistrationView):
    model = User
    serializer_class = UserRegisterSerializer
    response_keys = ['access',]
    access_keys = ['id', 'username', 'email','is_phone_verify','is_email_verify']
  

# --------------------------
"""
Authenticated user self-service view: 
Retrieve own profile : GET, PUT, PATCH, DELETE
Not allowed : POST
"""
# --------------------------
class UserView(APIView): 
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        request.user.delete()
        return Response({"detail": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

    def post(self, request, *args, **kwargs):
        return Response({"detail": "POST not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)