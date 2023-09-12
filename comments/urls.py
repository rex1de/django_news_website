from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path(r'^post/(?P<id>\d+)/(?P<slug>[-\w]+)/$', views.post_comment, name='post_comment')
]