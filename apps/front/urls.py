from django.urls import path
from . import views

app_name = 'front'

urlpatterns = [
    path('',views.index,name='index'),
    path('search/',views.search,name='search'),
    path('usearch/',views.upper_search,name='usearch'),
    path('list/',views.document_list,name='list'),
    path('show/', views.ShowView.as_view(), name='show'),
    path('author_bar/', views.AuthorChartView.as_view(), name='author_bar'),
    path('line/', views.YearChartView.as_view(), name='line'),
    path('orginize_bar/', views.OrginiseChartView.as_view(), name='orginize_bar'),
    path('xpie/', views.XuekeChartView.as_view(), name='xpie'),
    path('qbar/', views.QikanChartView.as_view(), name='qbar'),
    path('catpie/', views.CatChartView.as_view(), name='cat_pie'),
    path('word/', views.WordChartView.as_view(), name='word'),
    path('relation/', views.RelationChartView.as_view(), name='relation'),
    path('test/', views.test, name='test'),

]