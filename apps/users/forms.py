from django import forms
from apps.forms import FormMixin
# from utils import dxcache
from django.core import validators
from django.contrib.auth import get_user_model
User = get_user_model()


class LoginForm(forms.Form,FormMixin):
    username = forms.CharField(max_length=12,error_messages={'max_length':'请输入正确的用户名','min_length':'请输入正确的用户名'})
    pwd = forms.CharField(max_length=20,min_length=5,error_messages={'max_length':'密码不能超过20个字符','min_length':'密码不得少于5个字符'})
    # next = forms.CharField(max_length=100,required=False)
    # remember = forms.IntegerField(required=False)


class SignupForm(forms.Form,FormMixin):
    regname = forms.CharField(max_length=12,min_length=3,error_messages={'max_length': '请输入da正确的用户名', 'min_length': '请输入xiao正确的用户名'})
    regpass = forms.CharField(max_length=20, min_length=5,error_messages={'max_length': '密码不能超过20个字符', 'min_length': '密码不得少于5个字符'})
    reregpass = forms.CharField(max_length=20, min_length=5,error_messages={'max_length': '密码不能超过20个字符', 'min_length': '密码不得少于5个字符'})
    # sms_captcha = forms.CharField(max_length=6,min_length=6)
    # img_captcha = forms.CharField(max_length=4,min_length=4)
    # username = forms.CharField(max_length=50)

    def clean(self):
        cleaned_data = super(SignupForm, self).clean()
        regname = cleaned_data.get('regname')
        exists = User.objects.filter(username=regname).exists()
        if exists:
            raise forms.ValidationError('该用户已注册')
        password1 = cleaned_data.get('regpass')
        password2 = cleaned_data.get('reregpass')
        if password1 != password2:
            raise forms.ValidationError('两次输入的密码不一致')
        #
        # sms_captcha = cleaned_data.get('sms_captcha')
        # sms_captcha_mem = dxcache.get(telephone)
        # if not sms_captcha_mem or sms_captcha != sms_captcha_mem:
        #     raise forms.ValidationError('短信验证码错误')
        #
        # img_captcha = cleaned_data.get('img_captcha')
        # img_captcha_mem = dxcache.get(img_captcha)
        # if not img_captcha_mem or img_captcha!= img_captcha_mem:
        #     raise forms.ValidationError('图形验证码错误')
        return cleaned_data


class ModifyPwdForm(forms.Form):
    '''重置密码'''
    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)


class UploadImageForm(forms.ModelForm):
    '''用户更改图像'''
    class Meta:
        model = User
        fields = ['image']

class UserInfoForm(forms.ModelForm):
    '''个人中心信息修改'''
    class Meta:
        model = User
        fields = ['birthday','email','nick_name','mobile','gender']