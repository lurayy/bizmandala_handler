from rest_framework import serializers
from .models import Bundle, Price, Invoice

class BundleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bundle
        fields ='__all__'

class PriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Price
        fields ='__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields ='__all__'