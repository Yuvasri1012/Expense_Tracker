from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    INCOME = 'Income'
    EXPENSE = 'Expense'
    TYPE_CHOICES = [(INCOME, 'Income'), (EXPENSE, 'Expense')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    icon = models.CharField(max_length=10, default='📦')
    color = models.CharField(max_length=20, default='#94A3B8')

    class Meta:
        unique_together = ('user', 'name', 'type')
        verbose_name_plural = 'categories'

    def __str__(self):
        return f"{self.name} ({self.type})"


class Transaction(models.Model):
    INCOME = 'Income'
    EXPENSE = 'Expense'
    TYPE_CHOICES = [(INCOME, 'Income'), (EXPENSE, 'Expense')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transactions')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='transactions')
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.CharField(max_length=255)
    extra = models.TextField(blank=True, default='')
    date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f"{self.type}: {self.note} ₹{self.amount} on {self.date}"
