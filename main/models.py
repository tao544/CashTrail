from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models import Sum

# ------------------------
# USER MODEL
# ------------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('parent', 'Parent'),
        ('child', 'Child'),
    )

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='parent'
    )

    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='children'
    )

    def save(self, *args, **kwargs):

        # if user has a parent → they must be a child
        if self.parent:
            self.role = "child"

        # if user has no parent → they are a parent
        else:
            self.role = "parent"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

# ------------------------
# TRANSACTION MODEL
# ------------------------
class Transaction(models.Model):
    TRANSACTION_TYPE = (
        ('credit', 'Credit'),
        ('debit', 'Debit'),
    )

    child = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='transactions'
    )
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.child.username} - {self.category} - {self.amount}"


# ------------------------
# CHILD ACCOUNT MODEL
# ------------------------
class ChildAccount(models.Model):
    child = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='account'
    )
    allowance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    def total_spent(self):
        total = self.child.transactions.filter(transaction_type='debit').aggregate(Sum('amount'))['amount__sum']
        return total or 0

    def balance(self):
        credits = self.child.transactions.filter(transaction_type="credit").aggregate(Sum("amount"))["amount__sum"] or 0
        debits = self.child.transactions.filter(transaction_type="debit").aggregate(Sum("amount"))["amount__sum"] or 0
        return credits - debits

    def __str__(self):
        return f"{self.child.username} Account"