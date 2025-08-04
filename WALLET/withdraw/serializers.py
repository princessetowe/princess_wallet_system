from rest_framework import serializers
from user_reg.models import Withdraw

class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = Withdraw
        fields = '__all__'
        read_only_fields =['wallet', 'time_made', 'status']