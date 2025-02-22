from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import Customer
from .serializers import CustomerSerializer

# Create your views here.
class SignUpAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, format=None):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        try:
            data = request.data
            serializer = CustomerSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                email = data.get('email')
                account_num = data.get('account_num')


                if Customer.objects.filter(email__exact=email).exists():
                    return Response({'error': 'Email already in use'}, status=status.HTTP_400_BAD_REQUEST)
                elif Customer.objects.filter(account_num__exact=account_num).exists():
                    return Response({'error': 'Account number already exists'}, status=status.HTTP_400_BAD_REQUEST)
                
                else:
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)