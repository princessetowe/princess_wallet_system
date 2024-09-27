from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Signup
from .serializers import SignupSerializer
# Create your views here.
class SignupAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user = Signup.objects.all()
        serializer = SignupSerializer(user, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)