from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_http_methods
from erp.models import ERP
from erp_handler.settings import docker_ip, docker_port, docker_protocol
import requests
from django.shortcuts import render


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
        url = '{}://{}:{}/containers/json?all=1'.format('http','127.0.0.1', '2375')
        res = requests.get(url)
        containers = res.json()
        containers_list = []
        containers = containers[st:st+lmt]
        for container in containers:
            containers_list.append(
                {
                    'id': container['Id'],
                    'name': container['Names'][0],
                    'state': container['State'],
                    'status': container['Status'],
                }
            )
        return JsonResponse({'container_list' : containers_list}, status = 200)

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def list_erps(request):
    return render(request, 'list.html')

@login_required
def register_erp(request):
    return render(request, 'register.html')

