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
            start = converter(request.GET.get('start',''))
            limit = converter(request.GET.get('lmt',''))
            bill_amount_gte = converter(request.GET.get('bill_amount_gte',''))
            bill_amount_lte = converter(request.GET.get('bill_amount_lte',''))
            hours_lte = converter(request.GET.get('hours_lte',''))
            hours_gte = converter(request.GET.get('hours_gte',''))
            erp_gte = converter(request.GET.get('erp_gte',''))
            erp_lte = converter(request.GET.get('erp_lte',''))
            invoices = Invoice.objects.filter(user = request.user)
            if bill_amount_gte:
                invoices = invoices.filter(bill_amount__gte = bill_amount_gte)
            if bill_amount_lte:
                invoices = invoices.filter(bill_amount__lte = bill_amount_lte)
            if hours_gte:
                invoices = invoices.filter(hours__gte = hours_gte)
            if hours_lte:
                invoices = invoices.filter(hours__lte = hours_lte)
            if erp_gte:
                invoices = invoices.filter(number_of_erps__gte = erp_gte)
            if erp_lte:
                invoices = invoices.filter(number_of_erps__lte = erp_lte)
            if start == None:
                start = 0
            if limit == None:
                limit = 20
            invoices = invoices[start:start+limit]
            return JsonResponse({'status':True, 'invoices': invoices_to_json(invoices)})


    @method_decorator(for_logged_in())
    def post(self, request, uuid=None):
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        try:
            settings = Setting.objects.all()[0]
        except:
            raise Exception("Setting are not yet set. Please define setting from the admin panel.")
        data_json['hours'] = int(data_json['hours'])
        data_json['number_of_erps'] = int(data_json['number_of_erps'])
        if data_json['hours'] < settings.lowest_purchase_time_limit_in_hours:
            raise Exception('Purchased time must be at least ',settings.lowest_purchase_time_limit_in_hours)
        if data_json['pure_total_amount'] != (data_json['number_of_erps']*settings.unitary_price*data_json['hours']):
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
            hours = data_json['hours'],
            number_of_erps = data_json['number_of_erps'],
        )
        invoice.is_paid = True
        invoice.save()
        credits_ = []
        try:
            if data_json['extend_credit']:
                for credit_id in data_json['extend_credit']:
                    credit = Credit.objects.get(id = credit_id )
                    credit.hours_left = credit.hours_left+data_json['hours']
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
                        hours_left = data_json['hours'],
                        hours_used = 0
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
                if x.hours_left == data_json['hours']:
                    x.delete()
                else:
                    x.hours_left = x.hours_left - data_json['hours']
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