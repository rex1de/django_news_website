
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.news, name='news_detail'),
    re_path(r'^category/(?P<slug>[-\w]+)/$', views.category, name='category'),
    path('search/', views.search, name='search'),
]
