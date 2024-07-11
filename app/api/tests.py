from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from app.api.models import Wallet, Transaction


class TransactionAPITestCase(TestCase):

    def setUp(self):
        self.url = reverse('transactions')

    def test_create_valid_transaction(self):
        wallet = Wallet.objects.create(label='test', balance=0)
        data = {'txid': 'txid', 'wallet': wallet.id, 'amount': 100}
        response = self.client.post(self.url, data, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        self.assertEqual(Wallet.objects.get().balance, 100)

    def test_create_invalid_transaction(self):
        wallet = Wallet.objects.create(label='test', balance=1000)
        data = {'txid': 'txid', 'wallet': wallet.id, 'amount': -2000}
        response = self.client.post(self.url, data, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 0)
        self.assertEqual(Wallet.objects.get().balance, 1000)
