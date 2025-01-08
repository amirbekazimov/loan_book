from .models import Debt
from django.contrib.auth import get_user_model
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'password', 'is_creditor']

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            is_creditor=True
        )
        return user


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Debt
        fields = '__all__'

    def validate(self, data):
        if not self.context['request'].user.is_shop_owner:
            raise serializers.ValidationError("Only shop owners can assign creditors.")
        return data
