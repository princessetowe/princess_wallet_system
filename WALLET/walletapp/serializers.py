from rest_framework import serializers
from .models import Wallet

class WalletSerializer(serializers.ModelSerializer):
    customer_username = serializers.CharField(source='customer.user.username', read_only=True)
    class Meta:
        model = Wallet
        fields = '__all__'
        read_only_fields = ['customer']