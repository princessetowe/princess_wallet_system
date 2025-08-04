from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import LoginSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import AllowAny, IsAuthenticated

# Create your views here.
class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "message": "Login successful",
                "user_id": user.id,
                "email": user.email,
                "token": token.key,
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail":"Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    def post(self, request, *args, **kwargs):
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delet()
        logout(request)
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
