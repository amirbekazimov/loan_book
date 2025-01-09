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


class CreditorSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'phone_number']


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['id', 'username', 'first_name', 'phone_number']


class DebtSerializer(serializers.ModelSerializer):
    creditor = CreditorSerializer(required=False)
    customer = CustomerSerializer(required=False)

    class Meta:
        model = Debt
        fields = ['id', 'amount', 'due_date', 'description', 'is_paid', 'customer', 'creditor']

    def validate(self, data):
        if not self.context['request'].user.is_shop_owner:
            raise serializers.ValidationError("Only shop owners can assign creditors.")
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['creditor'] = user
        validated_data['customer'] = user
        return super().create(validated_data)
