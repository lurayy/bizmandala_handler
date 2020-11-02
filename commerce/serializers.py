from rest_framework import serializers
from .models import Setting, Invoice, Credit

class SettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Setting
        fields ='__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields ='__all__'   


class CreditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Credit
        fields ='__all__'   