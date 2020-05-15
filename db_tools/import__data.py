import os
import sys
import pandas as pd

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+'../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'zhiwangShow.settings')

import django
django.setup()

from apps.front.models import Document


df = pd.read_excel('data/test_data.xls',index_col='序号')



# print(df.head())
for index in range(df.shape[0]):
    d = Document()
    info = df.iloc[index]
    d.title = info['篇名']
    d.author = info['作者']
    d.author_location = info['作者单位']
    d.acticle_source = info['出处']
    d.summary = info['摘要']
    d.page_nums = info['页码']
    d.key_words = info['关键词']
    d.save()
    print("第%d条数据插入成功" % index)

print("测试数据库商品信息写入成功!")