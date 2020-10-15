from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm, LoginForm
from .models import UserBase

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')
    if request.method == "GET":
        form = LoginForm()
        return render(request, 'login.html', {'form':form})
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username = username, password = password)
            if user is not None:
                login(request,user)
                return HttpResponseRedirect('/dashboard')
            else:
                return HttpResponse("Username or password doesn't match")
        return HttpResponse("Invalid Form.")

def user_register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/dashboard')
    if request.method == "GET":
        form = UserForm()
        return render(request, 'register_user.html', {'form':form})
    else:
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponseRedirect('/dashboard')
        return HttpResponseRedirect('/user/register')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')
