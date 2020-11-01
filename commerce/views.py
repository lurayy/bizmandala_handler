from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.decorators import method_decorator
from commerce.models import Bundle, Price, Invoice
import json
from commerce.utils import for_everyone, for_mods_only, bundles_to_json, prices_to_json, converter

class BundleClassView(View):
    @method_decorator(for_everyone())
    def get(self, request, uuid=None):
        if uuid:
            bundle = Bundle.objects.get(uuid=uuid)
            response_json = {
                'status' : True,
                'bundle' : bundles_to_json([bundle])[0]
            }
            return JsonResponse(response_json)
        else:
            start = converter(request.GET.get('start',''))
            limit = converter(request.GET.get('lmt',''))
            price_gte = converter(request.GET.get('price_gte',''))
            price_lte = converter(request.GET.get('price_lte',''))
            days_lte = converter(request.GET.get('days_lte',''))
            days_gte = converter(request.GET.get('days_gte',''))
            erp_gte = converter(request.GET.get('erp_gte',''))
            erp_lte = converter(request.GET.get('erp_lte',''))
            bundles = Bundle.objects.all()
            if price_gte:
                bundles = bundles.filter(price__gte = price_gte)
            if price_lte:
                bundles = bundles.filter(price__lte = price_lte)
            if days_gte:
                bundles = bundles.filter(time_in_days__gte = days_gte)
            if days_lte:
                bundles = bundles.filter(time_in_days__lte = days_lte)
            if erp_gte:
                bundles = bundles.filter(number_of_erp__gte = erp_gte)
            if erp_lte:
                bundles = bundles.filter(number_of_erp__lte = erp_lte)
            if start == None:
                start = 0
            if limit == None:
                limit = 20
            bundles = bundles[start:start+limit]
            return JsonResponse({'status':True, 'bundles': bundles_to_json(bundles)})

    @method_decorator(for_mods_only())
    def post(self,request):
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        bundle = Bundle.objects.create(
            time_in_days = data_json['time_in_days'],
            number_of_erp = data_json['number_in_erp'],
            price = data_json['price']
        )
        response_json = {
            'status' : True,
            'bundle' : bundles_to_json([bundle])[0]
        }
        return JsonResponse(response_json)
    
    @method_decorator(for_mods_only())
    def patch(self,request, uuid):
        if uuid == None:
            raise Exception('UUID required.')
        bundle = Bundle.objects.get(uuid=uuid)
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        if data_json['time_in_days']:
            bundle.time_in_days = int(data_json['time_in_days'])
        if data_json['number_of_erp']:
            bundle.number_of_erp = int(data_json['number_of_erp'])
        if data_json['price']:
            bundle.price = int(data_json['price'])
        response_json = {
            'status' : True,
            'bundle' : bundles_to_json([bundle])[0]
        }
        return JsonResponse(response_json)
    
    @method_decorator(for_mods_only())
    def delete(self, request, uuid):
        if uuid == None:
            raise Exception('UUID required.')
        bundle = Bundle.objects.get(uuid=uuid)
        bundle.delete()
        return JsonResponse({'status' : True})

class PriceView(View):
    
    @method_decorator(for_everyone())
    def get(self, request, uuid=None):
        if uuid:
            price = Price.objects.get(uuid = uuid)
            response_json = {
                'status':True,
                'price' : prices_to_json([price])[0]
            }
            return JsonResponse(response_json)
        start = converter(request.GET.get('start',''))
        limit = converter(request.GET.get('lmt',''))
        price_gte = converter(request.GET.get('price_gte',''))
        price_lte = converter(request.GET.get('price_lte',''))
        erp_gte = converter(request.GET.get('erp_gte',''))
        erp_lte = converter(request.GET.get('erp_lte',''))
        prices = Price.objects.filter()
        if price_gte:
            prices = prices.filter(
                price__gte = price_gte
            )
        if price_lte:
            prices = prices.filter(
                price__lte = price_lte
            )
        if erp_gte:
            prices = prices.filter(
                erp_number__gte = erp_gte
            )
        if price_lte:
            prices = prices.filter(
                erp_number__lte = erp_lte
            )
        if not start:
            start = 0
        if not limit:
            limit = 20
        prices = prices[start:start+limit]
        response_json = {
            'status' : True,
            'prices' : prices_to_json(prices)
        }
        return JsonResponse(response_json)

    @method_decorator(for_mods_only())
    def post(self, request, uuid=None):
        if uuid:
            raise Exception('Doesnot take uuid for creation of new price model.')
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        price = Price.objects.create(
            erp_number = data_json['erp_number'],
            price = data_json['price']
        )
        response_json = {
            'status' : True,
            'price' : prices_to_json([price])[0]
        }
        return JsonResponse(response_json)
    
    @method_decorator(for_mods_only())
    def patch(self, request, uuid=None):
        if not uuid:
            raise Exception('UUID of the price is required for modifcation.')
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        price = Price.objects.get(uuid = uuid)
        if data_json['erp_number']:
            price.erp_number = data_json['erp_number']
        if data_json['price']:
            price.price = data_json['price']
        price.save()
        response_json = {
            'status' : True,
            'price' : prices_to_json([price])[0]
        }
        return JsonResponse(response_json)

    @method_decorator(for_mods_only())
    def delete(self, request, uuid):
        if uuid == None:
            raise Exception('UUID required.')
        price = Price.objects.get(uuid=uuid)
        price.delete()
        return JsonResponse({'status' : True})
