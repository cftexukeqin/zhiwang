from django.contrib import admin
from .models import Document
# Register your models here.


@admin.register(Document)  # 第一个参数可以是列表
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author','author_location','acticle_source','summary','key_words',)
    search_fields = ('title', 'author','author_location','acticle_source','summary','key_words',)
