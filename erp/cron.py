from erp.models import ERP
from commerce.models import Credit, Setting
from erp.models import TestModel
import datetime
def handle_credits():
    try:
        settings = Setting.objects.all()[0]
    except:
        print("Setting are not yet set. Please define setting from the admin panel.")
    for erp in ERP.objects.filter(is_running = True):
        try:
            if erp.credit.left_days <= -settings.lowest_purchase_time_limit_in_days:
                erp.stop_container()
            else:
                erp.credit.left_days = erp.credit.left_days - 1
                erp.credit.save()
        except Exception as exp:
            print(exp, erp.id)