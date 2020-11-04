from django.views import View
from django.http import JsonResponse
import json
from erp.models import ERP, get_container_data
from commerce.models import Credit
from erp_handler.settings import docker_ip, docker_port, docker_protocol
import requests
from erp.utils import erps_to_json
from django.utils.decorators import method_decorator
from commerce.utils import for_everyone, for_mods_only, invoices_to_json, for_logged_in, credits_to_json, converter

class ERPView(View):
    @method_decorator(for_logged_in())
    def get(self, request, uuid=None):
        if uuid:
            erp = ERP.objects.get(uuid = uuid, user=request.user)
            response_json = {
                'status' : True,
                'erp' : erps_to_json([erp])[0]
            }
            return JsonResponse(response_json)
        else:
            start = converter(request.GET.get('start',''))
            limit = converter(request.GET.get('lmt',''))
            company = (request.GET.get('company',''))
            address = (request.GET.get('address',''))
            if start==None:
                start = 0
            if limit == None:
                limit = 20
            erps = ERP.objects.filter(user = request.user)
            if company:
                erps = erps.filter(company__icontains = company)
            if address:
                address = erps.filter(address__icontains = address)
            response_json = {
                'status' : True,
                'erps' : erps_to_json(erps)
            }
            return JsonResponse(response_json)

    @method_decorator(for_logged_in())
    def post(self, request):
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        credit = Credit.objects.get(id = data_json['credit'], user=request.user)
        # if credit.erp:
            # raise Exception('Selected slow is already occupied by ERP of ',str(credit.erp.company))
        if credit.left_days == 0:
            raise Exception('Selected Slot has zero days left.')
        erp = None
        erp = ERP.objects.create(
            user = request.user,
            company = data_json['company'],
            address = data_json['address'],
            credit = credit
        )
        try:
            erp.create_container()
        except Exception as exp:
            if erp:
                print('ldetet')
                erp.stop_container()
                erp.delete_container()
                erp.delete()
            raise Exception(exp)
        response_json = {
            'status' : True,
            'erp' : erps_to_json([erp])
        }
        return JsonResponse(response_json)

    @method_decorator(for_logged_in())
    def delete(self, request, uuid):
        if uuid:
            erp = ERP.objects.get(uuid = uuid, user = request.user)
            erp.stop_container()
            erp.delete_container()
            erp.delete()
            response_json = {
                'status' : True,
            }
            return JsonResponse(response_json)
        else:
            raise Exception('UUID required.')

    @method_decorator(for_logged_in())
    def patch(self, request, uuid):
        if uuid:
            erp = ERP.objects.get(uuid = uuid, user = request.user)
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            if data_json['address']: 
                erp.address = data_json['address']
            if data_json['company']:
                erp.company = data_json['company']
            erp.save()
            response_json = {
                'status' : True,
                'erp' : erps_to_json([erp])[0]
            }
            return JsonResponse(response_json)
        else:
            raise Exception('UUID required.')


@for_logged_in()
def stop_container(request, uuid):
    erp = ERP.objects.get(uuid = uuid, user = request.user)
    erp.stop_container()
    response_json = {
        'status' : True
    }
    return JsonResponse(response_json)

@for_logged_in()
def start_container(request, uuid):
    erp = ERP.objects.get(uuid = uuid, user = request.user)
    erp.start_container()
    response_json = {
        'status' : True
    }
    return JsonResponse(response_json)
