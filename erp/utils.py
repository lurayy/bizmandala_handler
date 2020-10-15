from erp.models import ERP
from django.forms.models import model_to_dict 

def erps_to_json(erps):
    data = []
    for erp in erps:
        data.append(model_to_dict(erp))
    return data