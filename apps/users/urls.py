from django.urls import path
from .views import my_login,regist,my_logout

app_name = 'auth'

urlpatterns = [
    path('login/',my_login,name='login'),
    path('regist/',regist,name='regist'),
    path('logout/',my_logout,name='logout')
]