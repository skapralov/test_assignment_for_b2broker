from django.urls import path

from app.api.views import WalletListAPIView, TransactionAPIView

urlpatterns = [
    path('wallets', WalletListAPIView.as_view(), name='wallets'),
    path('transactions', TransactionAPIView.as_view(), name='transactions'),
]