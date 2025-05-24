from django.db import models
from django.conf import settings

class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account_number = models.CharField(max_length=20, unique=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    currency = models.CharField(max_length=10, choices=[('USD', 'USD'), ('EUR', 'EUR'), ('KZT', 'KZT'), ('GBP', 'GBP'), ('JPY', 'JPY'), ('RUB', 'RUB')], default='USD')
    card_number = models.CharField(max_length=16, unique=True)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=4)
    card_type = models.CharField(max_length=10, choices=[('Debit', 'Debit'), ('Credit', 'Credit')])
    credit_status = models.CharField(max_length=10, choices=[('approved', 'Approved'), ('denied', 'Denied')], default='denied')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Credit(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    duration_months = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')

class Transaction(models.Model):
    sender_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sent_transactions')
    receiver_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='received_transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('failed', 'Failed')], default='pending')
    blockchain_transaction_id = models.CharField(max_length=255, null=True, blank=True)
    transaction_date = models.DateTimeField(auto_now_add=True)

class Report(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=[('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('annual', 'Annual')])
    category = models.CharField(max_length=50)
    total_spending = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    report_date = models.DateTimeField(auto_now_add=True)
