from rest_framework import serializers
from .models import Account, Transaction, User


class AccountSerializer(serializers.ModelSerializer):
    """
    Serializer for the Account model.
    """

    class Meta:
        model = Account
        fields = ['id', 'iban', 'balance']


class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    """

    class Meta:
        model = Transaction
        fields = ['id', 'account', 'date', 'amount', 'transaction_type']


class CustomerSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model.
    """

    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'password', 'surname', 'profile_picture']
        extra_kwargs = {
            'password': {'write_only': True},  # Make the password write-only
        }
