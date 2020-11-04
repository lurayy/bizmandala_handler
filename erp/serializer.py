from rest_framework import serializers
from erp.models import ERP, PortMan

class ERPSerializer(serializers.ModelSerializer):
    class Meta:
        model = ERP
        fields ='__all__'

class PortManSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortMan
        fields ='__all__'
