import json 
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.views import View


class UserBaseView(View):

    def get(self,request):
        try:
            return JsonResponse({'status':True, 'user_info' : self.get_user_details(request.user)})
        except Exception as exp:       
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})

    def post(self,request):
        try:
            if request.user != None:
                json_str = request.body.decode(encoding='UTF-8')
                data_json = json.loads(json_str)
                user = authenticate(username = str(data_json['username']), password = str(data_json['password']))
                login(request, user)
                return JsonResponse({'status':True, 'user_info' : self.get_user_details(user)})
            else:
                return JsonResponse({'status':True, 'user_info' : self.get_user_details(request.user)})
        except Exception as exp:       
            return JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
    
    def get_user_details(self, user):
        data = {
            'username' : user.username,
            'email' : user.email
        }
        return data
    
    def put(self, request):
        print('this is put')
        return JsonResponse({'status': True})
    
    
    def delete(self, request):
        print('this is put')
        return JsonResponse({'status': True})
    
    
    def options(self, request):
        print('this is put')
        return JsonResponse({'status': True})
    
    
    def patch(self, request):
        print('this is put')
        return JsonResponse({'status': True})
