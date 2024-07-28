from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

IBAN_REGEX = r'^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$'


class Account(models.Model):
    """
    Model representing a bank account.

    Attributes:
    iban (str): The International Bank Account Number (IBAN) of the account.
    balance (decimal): The current balance of the account.
    """

    iban = models.CharField(
        max_length=34,
        unique=True,
        validators=[
            RegexValidator(
                regex=IBAN_REGEX,
                message='IBAN must be in the correct format'
            )
        ]
    )
    balance = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return self.iban


class Transaction(models.Model):
    """
    Model representing a transaction on a bank account.

    Attributes:
    account (ForeignKey): The account associated with the transaction.
    date (datetime): The date and time of the transaction.
    amount (decimal): The amount of the transaction.
    transaction_type (str): The type of the transaction (Deposit, Withdrawal, Transfer).
    """

    DEPOSIT = 'D'
    WITHDRAWAL = 'W'
    TRANSFER = 'T'

    TRANSACTION_TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER, 'Transfer'),
    ]

    account = models.ForeignKey(Account, related_name='transactions', on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    transaction_type = models.CharField(max_length=1, choices=TRANSACTION_TYPES)

    def __str__(self):
        return f"{self.get_transaction_type_display()} - {self.amount}"
