from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import UserReadSerializer,UserRegisterSerializer
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.exceptions import PermissionDenied,MethodNotAllowed
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

from .models import User
# Create your views here.

class UserView(ModelViewSet):
    queryset = User.objects.all() 
    permission_classes = [IsAuthenticated] 

    def get_serializer_class(self): 
        if self.request.method == 'GET':
                return UserReadSerializer
        
        if self.action == 'register':
            if self.request.method == 'POST':
                return UserRegisterSerializer
 
        if self.action == 'me': 
            if self.request.method in ['PUT', 'PATCH','DELETE','HEAD']:
                return UserRegisterSerializer
 
        raise MethodNotAllowed(self.request.method)
    
    def get_permissions(self):
        if self.action in ['list', 'register']:
            return [AllowAny()]
        return super().get_permissions()
    

    @action(detail=False, methods=['get', 'put', 'patch', 'delete','head'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """ 
        # details: Returns the currently authenticated user.
        """
        user = request.user

        if request.method in ['PUT', 'PATCH']:
            serializer = self.get_serializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(UserReadSerializer(user).data)

        if request.method == 'DELETE':
            user.delete()
            return Response({"detail": "Account deleted successfully"}, status=status.HTTP_204_NO_CONTENT)

        serializer = self.get_serializer(user)
        return Response(serializer.data)
     
    @action(detail=False,methods=['post'],permission_classes=[AllowAny])
    def register(self,request):
        """
        # action:  POST /register/
        # details: Create New User Data, Unauthenticated user
        """
        serialiser = self.get_serializer(data=request.data)
        serialiser.is_valid(raise_exception=True)
        user = serialiser.save()

        token_data = TokenObtainPairSerializer(data={
            "username": request.data["username"],  
            "password": request.data["password"]
        })
        token_data.is_valid(raise_exception=True)
        tokens = token_data.validated_data
        
        return Response({
            'message':"User register Success",
            'user':UserReadSerializer(user).data,
            'tokens':tokens,
        }, status=status.HTTP_201_CREATED)
 