from workers import task
from erp.models import ERP
from commerce.models import Credit, Setting

@task(schedule=1)
def handle_credits():
    print('called')
    try:
        settings = Setting.objects.all()[0]
    except:
        raise Exception("Setting are not yet set. Please define setting from the admin panel.")
    
    for erp in ERP.objects.filter(is_running = True):
        if erp.credit.left_days <= -settings.lowest_purchase_time_limit_in_days:
            erp.stop_container()
        else:
            erp.credit.left_days = erp.credit.left_days - 1
            erp.credit.save()