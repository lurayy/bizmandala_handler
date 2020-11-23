from django.db import models
from user_handler.models import UserBase
import uuid

class Invoice(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.ForeignKey(UserBase, on_delete=models.PROTECT)
    bill_amount = models.FloatField()
    paid_amount = models.FloatField()
    pure_total_amount = models.FloatField()
    discount_amount = models.FloatField(default=0)
    discount_note = models.TextField()
    
    payment_verification = models.TextField()
    
    hours = models.PositiveIntegerField()
    number_of_erps = models.PositiveIntegerField()

    is_refunded = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_paid = models.BooleanField(default=False)
    is_converted_to_credits = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user.username} {self.created_at}'
    

class Credit(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.ForeignKey(UserBase, on_delete=models.PROTECT)
    hours_left = models.IntegerField()
    hours_used = models.PositiveIntegerField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Setting(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4)
    unitary_price = models.FloatField()
    grace_period_in_hours = models.PositiveIntegerField(default=2*24)
    lowest_purchase_time_limit_in_hours = models.PositiveIntegerField(default=30*24)

    

'''
{
    hours
    number_of_erp
    is_bundle
    
    for_erp  = [erp_id]
}
'''