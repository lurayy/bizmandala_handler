from commerce.serializers import BundleSerializer, PriceSerializer, InvoiceSerializer
from django.views.decorators.csrf import ensure_csrf_cookie
from commerce.models import Bundle, Price, Invoice
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def for_everyone():
    def decorator(func):
        @ensure_csrf_cookie
        def wrapper(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except Exception as exp: 
                res = JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'}, status=400)
                return res
        return wrapper
    return decorator

def for_mods_only():
    def decorator(func):
        @ensure_csrf_cookie
        def wrapper(request, *args, **kwargs):
            try:
                if not request.user.is_authenticated:
                    return JsonResponse({'status':False,'error': 'Unauthorized access.'}, status=403)
                if request.user.is_mod:
                    return func(request, *args, **kwargs)
                else:
                    return JsonResponse({'status':False,'error': 'Unauthorized access.'}, status=403)
            except Exception as exp: 
                res = JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'}, status=400)
                return res
        return wrapper
    return decorator

def bundles_to_json(bundles):
    data = []
    for bundle in bundles:
        temp = BundleSerializer(bundle).data
        data.append(temp)
    return data

def converter(value):
    try:
        return(abs(float(value)))
    except:
        return None


def prices_to_json(prices):
    data = []
    for price in prices:
        temp  = PriceSerializer(price).data
        data.append(temp)
    return data
