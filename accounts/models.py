from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.core.validators import MinValueValidator, RegexValidator

IBAN_REGEX = r'^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$'


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        'User',
        related_name="%(class)s_created_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    updated_by = models.ForeignKey(
        'User',
        related_name="%(class)s_updated_by",
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        abstract = True


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


class User(BaseModel, AbstractUser):
    """
    The User model extends the AbstractUser model to provide custom user functionalities.
    """

    email = models.EmailField(
        blank=False,
        unique=True,
        error_messages={'unique': 'This Email already has an account.'}
    )
    username = models.CharField(max_length=150, null=True, blank=True)
    surname = models.CharField(max_length=150, null=True, blank=True)
    password = models.CharField(max_length=150, null=True, blank=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
    profile_picture = models.ImageField(upload_to='photos/', null=True, blank=True)
