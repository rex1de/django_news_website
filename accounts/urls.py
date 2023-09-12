
from django.urls import path, re_path, include
from . import views

urlpatterns = [
    path('accounts/register/', views.register, name='register'),
    path('accounts/profile/', views.profile, name='profile'),
    re_path(r'^accounts/profile/(?P<id>\d+)$', views.guest_page, name='guest_page')

]