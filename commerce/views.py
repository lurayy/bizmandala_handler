from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.utils.decorators import method_decorator
from commerce.models import Setting, Invoice
import json
from commerce.utils import for_everyone, for_mods_only, settings_to_json, converter

class SettingView(View):
    
    @method_decorator(for_everyone())
    def get(self, request, uuid=None):
        settings = Setting.objects.all()[0]
        response_json = {
            'status' : True,
            'setting' : settings_to_json([settings])[0]
        }
        return JsonResponse(response_json)

    @method_decorator(for_mods_only())
    def post(self, request, uuid=None):
        if uuid:
            raise Exception('Doesnot take uuid for creation of new price model.')
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        settings = Setting.objects.create(
            unitary_price = data_json['unitary_price']
        )
        response_json = {
            'status' : True,
            'settings' : settings_to_json([settings])[0]
        }
        return JsonResponse(response_json)

    @method_decorator(for_mods_only())
    def patch(self, request, uuid=None):
        if not uuid:
            raise Exception('UUID of the price is required for modifcation.')
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        settings = Setting.objects.get(uuid = uuid)
        if data_json['unitary_price']:
            settings.unitary_price = data_json['unitary_price']
        settings.save()
        response_json = {
            'status' : True,
            'settings' : settings_to_json([settings])[0]
        }
        return JsonResponse(response_json)

    @method_decorator(for_mods_only())
    def delete(self, request, uuid):
        if uuid == None:
            raise Exception('UUID required.')
        settings = Setting.objects.get(uuid=uuid)
        settings.delete()
        return JsonResponse({'status' : True})
