from erp.models import ERP
from erp.serializer import ERPSerializer, PortManSerializer
from erp.models import get_container_data
import json
from commerce.utils import credits_to_json
def erps_to_json(erps):
    data = []
    for erp in erps:
        temp = ERPSerializer(erp).data
        container_data = get_container_data('erp_'+str(erp.id))
        temp['state'] = container_data[0]['State']
        temp['status'] = container_data[0]['Status']
        temp['credits'] = credits_to_json([erp.credit])[0]
        data.append(temp)
    return data