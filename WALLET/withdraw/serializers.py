from rest_framework import serializers
from user_reg.models import Transactions
class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transactions
        fields = ["amount"]

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive")
        return value
