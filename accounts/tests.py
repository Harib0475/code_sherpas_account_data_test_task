from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Account, Transaction


class AccountTests(APITestCase):
    def setUp(self):
        self.account = Account.objects.create(iban='GB33BUKB20201555555555', balance=1000.00)
        self.account2 = Account.objects.create(iban='GB94BARC20201530093459', balance=500.00)

    def test_create_account(self):
        url = reverse('account-list')
        data = {'iban': 'DE89370400440532013000', 'balance': 1000.00}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_accounts(self):
        url = reverse('account-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)

    def test_retrieve_account(self):
        url = reverse('account-detail', args=[self.account.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['iban'], self.account.iban)

    def test_update_account(self):
        url = reverse('account-detail', args=[self.account.id])
        data = {'iban': self.account.iban, 'balance': 2000.00}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 2000.00)

    def test_delete_account(self):
        url = reverse('account-detail', args=[self.account.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Account.objects.filter(id=self.account.id).exists())

    def test_deposit(self):
        url = reverse('account-deposit', args=[self.account.id])
        data = {'amount': 500.00}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 1500.00)

    def test_withdraw(self):
        url = reverse('account-withdraw', args=[self.account.id])
        data = {'amount': 500.00}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, 500.00)

    def test_withdraw_insufficient_funds(self):
        url = reverse('account-withdraw', args=[self.account.id])
        data = {'amount': 1500.00}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_transfer(self):
        url = reverse('account-transfer')
        data = {'from_iban': self.account.iban, 'to_iban': self.account2.iban, 'amount': 500.00}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.account.refresh_from_db()
        self.account2.refresh_from_db()
        self.assertEqual(self.account.balance, 500.00)
        self.assertEqual(self.account2.balance, 1000.00)

    def test_transfer_insufficient_funds(self):
        url = reverse('account-transfer')
        data = {'from_iban': self.account.iban, 'to_iban': self.account2.iban, 'amount': 1500.00}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_transactions(self):
        Transaction.objects.create(account=self.account, amount=100.00, transaction_type=Transaction.DEPOSIT)
        url = reverse('transaction-list', args=[self.account.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 6)
