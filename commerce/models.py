from django.db import models
from user_handler.models import UserBase
# Create your models here.

class Plan(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.FloatField(default=10)
    duration = models.PositiveIntegerField(default=1)  #always in days

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} {self.duration}'

class PaymentMethod(models.Model):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

class Payment(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.PROTECT, related_name='payments')
    plan = models.ForeignKey(Plan, on_delete = models.PROTECT)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.PROTECT)
    payment_verification = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
