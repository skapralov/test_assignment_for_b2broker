from django.db import transaction, IntegrityError
from django.db.models import F
from rest_framework.exceptions import ValidationError
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework_json_api import filters, django_filters

from app.api.models import Wallet, Transaction
from app.api.serializers import WalletSerializer, TransactionSerializer


class WalletListAPIView(ListAPIView, CreateAPIView):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    filter_backends = [
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend,
    ]
    filterset_fields = {
        'id': ('exact', ),
        'label': ('icontains', 'iexact', ),
    }
    ordering_fields = ['id', 'label']
    ordering = ['id']


class TransactionAPIView(ListAPIView, CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [
        filters.OrderingFilter,
        django_filters.DjangoFilterBackend,
    ]
    filterset_fields = {
        'id': ('exact', ),
        'txid': ('exact', ),
        'wallet_id': ('exact', ),
    }
    ordering_fields = ['id', ]
    ordering = ['id', ]

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        try:
            wallet = serializer.validated_data['wallet']
            wallet.balance = F('balance') + serializer.validated_data['amount']
            wallet.save()
        except IntegrityError:
            raise ValidationError('Balance cannot be less than 0')

        serializer.save()
