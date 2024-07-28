from django.core.management.base import BaseCommand
from accounts.models import Account, Transaction
import random
from faker import Faker


class Command(BaseCommand):
    """
    Django's management command to populate the database with dummy data.
    """

    help = 'Populate the database with dummy data'

    def handle(self, *args, **kwargs):
        faker = Faker()
        accounts = []
        for _ in range(10):
            iban = faker.iban()
            balance = random.uniform(1000, 5000)
            account = Account.objects.create(iban=iban, balance=balance)
            accounts.append(account)

        transaction_types = [Transaction.DEPOSIT, Transaction.WITHDRAWAL, Transaction.TRANSFER]

        for account in accounts:
            for _ in range(random.randint(5, 15)):
                amount = random.uniform(10, 1000)
                transaction_type = random.choice(transaction_types)
                if transaction_type == Transaction.TRANSFER:
                    other_account = random.choice([acc for acc in accounts if acc != account])
                    Transaction.objects.create(account=account, amount=-amount, transaction_type=transaction_type)
                    Transaction.objects.create(account=other_account, amount=amount, transaction_type=transaction_type)
                    account.balance -= amount
                    other_account.balance += amount
                    account.save()
                    other_account.save()
                else:
                    if transaction_type == Transaction.WITHDRAWAL and account.balance < amount:
                        amount = account.balance
                    Transaction.objects.create(account=account, amount=amount, transaction_type=transaction_type)
                    if transaction_type == Transaction.DEPOSIT:
                        account.balance += amount
                    else:
                        account.balance -= amount
                    account.save()

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with dummy data'))
