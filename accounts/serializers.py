from rest_framework import serializers
from .models import Account, Transaction


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
