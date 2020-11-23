from commerce.serializers import SettingSerializer, InvoiceSerializer, CreditSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from commerce.models import Setting, Invoice
from django.http import JsonResponse
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer

def for_everyone():
    def decorator(func):
        @ensure_csrf_cookie
        def wrapper(request, *args, **kwargs):
            try:
                try:
                    data = {'token':request.headers['Authorization'].split(' ')[0]}
                    valid_data = VerifyJSONWebTokenSerializer().validate(data)
                    user = valid_data['user']
                except:
                    user = None
                request.user = user
                return func(request, *args, **kwargs)
            except Exception as exp: 
                res = JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
                return res
        return wrapper
    return decorator

def for_mods_only():
    def decorator(func):
        @ensure_csrf_cookie
        def wrapper(request, *args, **kwargs):
            try:
                try:
                    data = {'token':request.headers['Authorization'].split(' ')[0]}
                    valid_data = VerifyJSONWebTokenSerializer().validate(data)
                    user = valid_data['user']
                except:
                    user = None
                request.user = user
                if not request.user:
                    return JsonResponse({'status':False,'error': 'You are not logged in.'}, status=403)
                if request.user.is_mod:
                    return func(request, *args, **kwargs)
                else:
                    return JsonResponse({'status':False,'error': 'Unauthorized access.'}, status=403)
            except Exception as exp: 
                res = JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
                return res
        return wrapper
    return decorator

def for_logged_in():
    def decorator(func):
        @ensure_csrf_cookie
        def wrapper(request, *args, **kwargs):
            try:
                try:
                    data = {'token':request.headers['Authorization'].split(' ')[0]}
                    valid_data = VerifyJSONWebTokenSerializer().validate(data)
                    user = valid_data['user']
                except:
                    user = None
                request.user = user
                if not request.user:
                    return JsonResponse({'status':False,'error': 'You are not logged in.'}, status=403)
                else:
                    return func(request, *args, **kwargs)
            except Exception as exp: 
                res = JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
                return res
        return wrapper
    return decorator

def converter(value):
    try:
        return(abs(float(value)))
    except:
        return None


def settings_to_json(settings):
    data = []
    for setting in settings:
        temp  = SettingSerializer(setting).data
        data.append(temp)
    return data

def invoices_to_json(invoices):
    data = []
    for invoice in invoices:
        temp = InvoiceSerializer(invoice).data
        data.append(temp)
    return data

def credits_to_json(credits):
    data = []
    for credit in credits:
        temp = CreditSerializer(credit).data
        try:
            temp['erp'] = credit.erp.uuid
            temp['erp_company'] = credit.erp.company
        except:
            temp['erp'] = None
            temp['erp_company'] = "Not Assigned"
        data.append(temp)
    return data