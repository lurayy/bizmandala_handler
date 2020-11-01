from commerce.utils import for_everyone, for_mods_only, invoices_to_json, for_logged_in
from django.utils.decorators import method_decorator
from django.views import View
from commerce.models import Bundle, Price, Invoice, Credit
from django.http import JsonResponse
import json

class InvoiceView(View):
    @method_decorator(for_logged_in())
    def get(self, request, uuid):
        if uuid:
            invoice = Invoice.objects.get(uuid = uuid, user = request.user)
            response_json = {
                'status' : True,
                'invoice' : invoices_to_json([invoice])[0]
            }
            return JsonResponse(response_json)
    
    @method_decorator(for_logged_in())
    def post(self, request):
        pass
    
    @method_decorator(for_logged_in())
    def patch(self, request, uuid):
        if uuid == None:
            raise Exception('UUID required.')
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        if data_json['do'] == 'refund':
            pass
        response_json = {
            'status' : True,
            'msg' : 'Payment refunded.'
        }
        return JsonResponse(response_json)

