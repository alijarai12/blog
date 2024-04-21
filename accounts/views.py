from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.serializers import AuthTokenSerializer
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


# Generate Token Manually
def get_tokens_for_user(user):
  refresh = RefreshToken.for_user(user)
  return {
      'refresh': str(refresh),
      'access': str(refresh.access_token),
  }

# Register API
class UserRegistrationView(APIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = get_tokens_for_user(user)
        return Response({'token':token, 'msg':'Registration Successful'}, status=status.HTTP_201_CREATED)

from rest_framework.exceptions import AuthenticationFailed


class UserLoginView(APIView):

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        # Check if authentication was successful
        if user is not None:
            # Generate tokens for authenticated user
            token = get_tokens_for_user(user)
            return Response({'token': token, 'msg': 'Login Successful'}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid credentials."},
                            status=status.HTTP_401_UNAUTHORIZED)
        
