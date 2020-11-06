from erp.models import ERP

def start_all_contaiers():
    for erp in ERP.objects.filter(is_running=True):
        erp.start_container()
