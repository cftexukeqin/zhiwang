from django.db import models

# Create your models here.

class Document(models.Model):
    title = models.CharField(max_length=200,default="")
    author = models.CharField(max_length=200,default="")
    author_location = models.TextField(default="")
    acticle_source = models.CharField(max_length=200,default="")
    page_nums = models.CharField(max_length=50,default="")
    summary = models.TextField(default="")

    key_words = models.CharField(max_length=200,default="")
    add_time = models.DateTimeField(auto_now_add=True)