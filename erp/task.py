from background_task import background
from erp.models import ERP
from commerce.models import Credit

@background()
def handle_credits():
    for erp in ERP.objects.filter(is_running = True):
        if erp.credit.left_days <= 0:
            erp.stop_container()
        else:
            erp.credit.left_days = erp.credit.left_days - 1
            erp.credit.save()