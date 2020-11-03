from commerce.utils import for_everyone, for_mods_only, invoices_to_json, for_logged_in, credits_to_json, converter
from django.utils.decorators import method_decorator
from django.views import View
from commerce.models import Setting, Invoice, Credit
from django.http import JsonResponse
import json

class InvoiceView(View):
    @method_decorator(for_logged_in())
    def get(self, request, uuid=None):
        if uuid:
            invoice = Invoice.objects.get(uuid = uuid, user = request.user)
            response_json = {
                'status' : True,
                'invoice' : invoices_to_json([invoice])[0]
            }
            return JsonResponse(response_json)
        else:
            return JsonResponse({'asdf' : 'asfd'})

    @method_decorator(for_logged_in())
    def post(self, request, uuid=None):
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        settings = Setting.objects.all()[0]
        if data_json['pure_total_amount'] != (data_json['number_of_erps']*settings.unitary_price*data_json['time_in_days']):
            raise Exception('Pure total amount miscalculated.')
        if data_json['paid_amount'] != data_json['bill_amount']:
            raise Exception('Billed amount is not equal to the paid amount.')
        invoice = Invoice.objects.create(
            user = request.user,
            bill_amount = data_json['bill_amount'],
            paid_amount = data_json['paid_amount'],
            pure_total_amount = data_json['pure_total_amount'],
            discount_amount = data_json['discount_amount'],
            discount_note = data_json['discount_note'],
            payment_verification = data_json['payment_verification'],
            time_in_days = data_json['time_in_days'],
            number_of_erps = data_json['number_of_erps'],
            is_bundle = data_json['is_bundle']
        )
        invoice.is_paid = True
        invoice.save()
        credits_ = []
        try:
            if data_json['extend_credit']:
                for credit_id in data_json['extend_credit']:
                    credit = Credit.objects.get(id = credit_id )
                    credit.left_days = credit.left_days+data_json['time_in_days']
                    credit.save()
                    credits_.append(credit)
            try:
                top_len = len(data_json['extend_credit'])
            except:
                top_len = 0
            x = data_json['number_of_erps'] - top_len
            if x > 0:
                for _ in range (x):
                    credit = Credit.objects.create(
                        user = request.user,
                        left_days = data_json['time_in_days'],
                        used_days = 0
                    )
                    credits_.append(credit)
            response_json = {
                'status' : True,
                'invoice' : invoices_to_json([invoice]),
                'credits' : credits_to_json(credits_)
            }
            invoice.is_converted_to_credits = True
            invoice.save()
            return JsonResponse(response_json)
        except Exception as exp:
            for x in credits_:
                if x.left_days == data_json['time_in_days']:
                    x.delete()
                else:
                    x.left_days = x.left_days - data_json['time_in_days']
                    x.save()
            raise Exception(exp)

    @method_decorator(for_logged_in())
    def patch(self, request, uuid=None):
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


class CreditView(View):
    @method_decorator(for_logged_in())
    def get(self, request, uuid=None):
        if uuid:
            credit = Credit.objects.get(uuid = uuid, user=request.user)
            response_json = {
                'status' :True,
                'credit' : credits_to_json([credit])[0]
            }
            return JsonResponse(response_json)
        else:
            start = converter(request.GET.get('start',''))
            limit = converter(request.GET.get('lmt',''))
            if start == None:
                start = 0
            if limit == None:
                limit = 20
            credit_s = Credit.objects.filter()[start:start+limit]
            response_json = {
                'status' : True,
                'credits' : credits_to_json(credit_s)
            }
            return JsonResponse(response_json)

