from django.views import View
from django.http import JsonResponse
import json

class Container(View):

    def get(self, request):
        container_list = [
            'asdf','asdf'
        ]
        return JsonResponse({'container_list' : container_list}, status = 200)
    
    def create(self, request):
        json_str = request.body.decode(encoding='UTF-8')
        data_json = json.loads(json_str)