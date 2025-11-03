from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny 
from rest_framework_simplejwt.tokens import RefreshToken
 
class BaseRegistrationView(APIView):
    """
    Base registration handler for creating users and returning JWT tokens.

    Usage:
        - Set `serializer_class`
        - Define `response_keys` to include user fields or tokens in response
        - Define `access_keys` to embed extra claims inside access token

    Example:
        response_keys = ['id', 'username', 'email', 'access', 'refresh']
        access_keys = ['id', 'username', 'email']
    """
    
    serializer_class = None
    model = None
    response_keys = []          # Response Fileds 
    access_keys = []            # Fields to add to access token
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        if not self.serializer_class:
            raise Exception("serializer_class must be set.")

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Add custom fields to access token
        for field in self.access_keys:
            if hasattr(user, field):
                access_token[field] = getattr(user, field)

        # Prepare response json keys
        response_data = {}
        for key in self.response_keys:
            if key == 'access':
                response_data['access'] = str(access_token)
            elif key == 'refresh':
                response_data['refresh'] = str(refresh)
            elif hasattr(user, key):
                response_data[key] = getattr(user, key)

        return Response(response_data, status=status.HTTP_201_CREATED)