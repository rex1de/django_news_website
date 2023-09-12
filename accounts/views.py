from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
# Create your views here.

def register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        user = User.objects.create_user(username=username, email=email, password=pwd)
        login(request=request, user=user)
        return redirect('main:index')

@login_required
def profile(request):
    return render(request, 'registration/profile.html')

def guest_page(request, id):
    profile = get_object_or_404(Profile, id=id)
    return render(request, 'registration/guest_page.html', {'profile': profile})