from django.db import models
from django.contrib.auth.models import User

class FinancialRecord(models.Model):
    TRANSACTION_TYPES = [('INCOME', 'Income'), ('EXPENSE', 'Expense')]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    record_type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.record_type}: {self.amount} ({self.category})"
