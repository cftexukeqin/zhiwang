from django.contrib import admin
from .models import UserProfile


# Register your models here.

@admin.register(UserProfile)  # 第一个参数可以是列表
class BookAdmin(admin.ModelAdmin):
    list_display = ('nick_name', 'mobile', 'email','is_staff','image',)
    search_fields = ('nick_name', 'mobile')
