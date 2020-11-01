from django.db import models
from user_handler.models import UserBase
from erp.models import ERP
import uuid

class Bundle(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    time_in_days = models.PositiveIntegerField(default = 30)
    number_of_erp = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=1000.00)

    class Meta:
        unique_together = [['time_in_days', 'number_of_erp', 'price']]
    
    def __str__(self):
        return f'{self.time_in_days} {self.number_of_erp} {self.price}'

class Price(models.Model):
    '''Price of erp for 1 day'''
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    erp_number = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=1000)

    class Meta:
        unique_together = [['erp_number',]]

class Invoice(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.ForeignKey(UserBase, on_delete=models.PROTECT)
    bill_amount = models.FloatField()
    paid_amount = models.FloatField()
    pure_total_amount = models.FloatField()
    discount_amount = models.FloatField(default=0)
    discount_note = models.TextField()
    
    time_in_days = models.PositiveIntegerField()
    number_of_erp = models.PositiveIntegerField()
    is_bundle = models.BooleanField(default=False)

    is_refunded = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} {self.created_at}'
    

class Credit(models.Model):
    user = models.ForeignKey(UserBase, on_delete=models.PROTECT)
    erp = models.ForeignKey(ERP, on_delete=models.SET_NULL, null=True, blank=True)
    left_days = models.PositiveIntegerField()
    used_days = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

