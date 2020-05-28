from django.urls import path
from .views import my_login,regist,my_logout,UserinfoView,ModifyPwdView,UploadImageView

app_name = 'auth'

urlpatterns = [
    path('login/',my_login,name='login'),
    path('regist/',regist,name='regist'),
    path('logout/',my_logout,name='logout'),
    path("info/", UserinfoView.as_view(), name='info'),
    path("resetpwd/", ModifyPwdView.as_view(), name='resetpwd'),
    # 用户图像上传
    path("image/upload/", UploadImageView.as_view(), name='image_upload'),
]