import json 
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token
from django.shortcuts import render
from user_handler.models import Profile
from django.views.decorators.csrf import ensure_csrf_cookie

def try_catch_dec():
    def decorator(func):
        @ensure_csrf_cookie
        def wrapper(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except Exception as exp: 
                res = JsonResponse({'status':False,'error': f'{exp.__class__.__name__}: {exp}'})
                return res
        return wrapper
    return decorator
    

class UserBaseView(View):

    @method_decorator(try_catch_dec())
    def get(self,request):
        res = JsonResponse({'status':True, 'user_info' : self.get_user_details(request.user)})
        return res
    
    @method_decorator(try_catch_dec())
    def post(self,request):
        if request.user != None:
            json_str = request.body.decode(encoding='UTF-8')
            data_json = json.loads(json_str)
            user = authenticate(username = str(data_json['username']), password = str(data_json['password']))
            login(request, user)
            return JsonResponse({'status':True, 'user_info' : self.get_user_details(user)})
        else:
            return JsonResponse({'status':True, 'user_info' : self.get_user_details(request.user)})
    
    def get_user_details(self, user):
        if user != None:
            data = {
                'username' : user.username,
                'email' : user.email,
                'address' : user.profile.address,
                'phone_number' : user.profile.phone_number,
                'phone_number2' : user.profile.phone_number2,
                'profile_image' : str(user.profile.profile_image),
                'post' : user.profile.post,
                'is_verified' : user.is_verified,
                'first_name' : user.first_name,
                'last_name' : user.last_name
            }
        else:
            data = {
                'user' : 'None'
            }
        return data
    
    @method_decorator(try_catch_dec())
    def put(self, request):
        return JsonResponse({'status': True})
    
    @method_decorator(try_catch_dec())
    def delete(self, request):
        print('this is delete')
        return JsonResponse({'status': True})

    @method_decorator(try_catch_dec())
    def patch(self, request):
        return JsonResponse({'status': True})


def f404(request):
    return render(request,'404.html')