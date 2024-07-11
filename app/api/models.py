from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, CheckConstraint


class Wallet(models.Model):
    label = models.CharField(max_length=255)
    balance = models.DecimalField( max_digits=32, decimal_places=18, validators=[MinValueValidator(0)])

    class Meta:
        db_table = 'wallets'
        constraints = [
            CheckConstraint(
                check=Q(balance__gte=0),
                name='check_positive_balance',
            ),
        ]


class Transaction(models.Model):
    txid = models.CharField(max_length=255, unique=True)  # noqa
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=32, decimal_places=18)

    class Meta:
        db_table = 'transactions'
