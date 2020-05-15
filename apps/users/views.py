from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login,logout,authenticate
from .forms import LoginForm,SignupForm

from .models import UserProfile
from apps.utils import restful

# Create your views here.

def my_login(request):
    if request.method == "GET":
        return render(request, 'auth/auth.html')
    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('pwd')
            next = form.cleaned_data.get("next")
            if next:
                next_url = next.split("=")[1]
            else:
                next_url = ""
            user = authenticate(request,username=username,password=password)
            # print("user",user)
            if user:
                login(request,user)
                request.session.set_expiry(None)
                data = {
                    "next_url":next_url
                }
                return restful.result(data=data)
            else:
                return restful.noauth(message="用户名或者密码错误!")
        else:
            print(form.get_error())
            return restful.paramserror(form.get_error())

def regist(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('regname')
            pwd1 = form.cleaned_data.get('regpass')
            # pwd2 = form.cleaned_data.get('pwd2')
            user = UserProfile.objects.create_user(username=name,password=pwd1)
            login(request, user)
            return restful.ok()
        else:
            return restful.paramserror(form.get_error())



def my_logout(request):
    logout(request)
    return redirect(reverse('auth:login'))