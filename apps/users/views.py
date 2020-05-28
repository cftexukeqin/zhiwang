from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login,logout,authenticate
from .forms import LoginForm,SignupForm,UploadImageForm, ModifyPwdForm, UserInfoForm
from django.contrib.auth.hashers import make_password
from django.views.generic import View

from .models import UserProfile
from apps.utils import restful
from apps.utils.mixin_utils import LoginRequiredMixin
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




class ModifyPwdView(View):
    '''修改用户密码'''

    def post(self, request):
        modify_form = ModifyPwdForm(request.POST)
        if modify_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            email = request.POST.get("email", "")
            if pwd1 != pwd2:
                return restful.paramserror(message="两次密码不一致")
            user = UserProfile.objects.get(email=email)
            user.password = make_password(pwd2)
            user.save()

            return restful.ok()
        else:
            email = request.POST.get("email", "")
            return restful.paramserror(message="密码不正确！")


class UserinfoView(LoginRequiredMixin, View):
    """
    用户个人信息
    """

    def get(self, request):
        return render(request, 'auth/usercenter.html')

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        print(user_info_form)
        if user_info_form.is_valid():
            user_info_form.save()
            return restful.ok()
        else:
            return restful.paramserror(message="参数错误")


class UploadImageView(LoginRequiredMixin, View):
    '''用户图像修改'''

    def post(self, request):
        # 上传的文件都在request.FILES里面获取，所以这里要多传一个这个参数
        image_form = UploadImageForm(request.POST, request.FILES)
        if image_form.is_valid():
            image = image_form.cleaned_data['image']
            request.user.image = image
            request.user.save()
            return restful.ok()
        else:
            return restful.paramserror(message="参数错误")
