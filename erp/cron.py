from erp.models import ERP
from commerce.models import Credit, Setting
import datetime

def handle_credits():
    try:
        settings = Setting.objects.all()[0]
    except:
        print("Setting are not yet set. Please define setting from the admin panel.")
    for erp in ERP.objects.filter(is_running = True):
        try:
            if erp.credit.hours_left <= -settings.lowest_purchase_time_limit_in_hours:
                erp.stop_container()
            else:
                erp.credit.hours_left = erp.credit.hours_left - 1
                erp.credit.save()
        except Exception as exp:
            print("error ",exp, erp.id)
