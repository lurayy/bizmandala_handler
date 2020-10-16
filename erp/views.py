from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from erp.models import ERP, get_container_data
from erp_handler.settings import docker_ip, docker_port, docker_protocol
import requests
from django.shortcuts import render
from erp.utils import erps_to_json

class Container(View):

    def get(self, request):
        try:
            st = int(request.GET['st'])
        except:
            st = 0
        try: 
            lmt = int(request.GET['lmt'])
        except:
            lmt = 10
        erps = ERP.objects.filter(user__id = request.user.id)
        erps = erps[st:st+lmt]
        response_json = {'status':False, 'erps':[]}
        for erp in erps_to_json(erps):
            data = get_container_data('erp_'+str(erp['id']))
            response_json['erps'].append({
                'company' : erp['company'],
                'address' : erp['address'],
                'link' : erp['link'],
                'data' : data
                # 'state' : data['State'],
                # 'status' : data['Status']
            })
        return JsonResponse(response_json)

@login_required
def create(request):
    if request.method == "POST":
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)
        erp = ERP.objects.create(
            user = request.user,
            company = data_json['company'],
            address = data_json['address']
        )
        erp.create_container()
        return JsonResponse({'status':True}, status = 200)
    else:
        return JsonResponse( {'status':False}, status=502)

@login_required
def stop(request, id):
    print(id)
    return JsonResponse({'status':True})

@login_required
def start(request, id):
    print(id)
    return JsonResponse({'status':True})

@login_required
def delete(request, id):
    print(id)
    return JsonResponse({'status':True})




@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def list_erps(request):
    return render(request, 'list.html')

@login_required
def register_erp(request):
    return render(request, 'register.html')

