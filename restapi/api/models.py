from django.db import models
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    cache = models.FloatField(default=0)


class Transaction(models.Model):
    INCOME_TYPE = 'income'
    EXPENSE_TYPE = 'expense'
    TRANSACTION_TYPES = [
        (INCOME_TYPE, 'Income'),
        (EXPENSE_TYPE, 'Expense'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    amount = models.FloatField(validators=[MinValueValidator(1)])
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=100)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.type} - {self.amount}'
