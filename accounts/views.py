from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from social_django.models import UserSocialAuth
from django.contrib.auth.backends import ModelBackend
# Create your views here.


def register(request):
    if request.method == 'GET':
        return render(request, 'registration/register.html')
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        user = User.objects.create_user(
            username=username, email=email, password=pwd, first_name=first_name, last_name=last_name)
        login(request=request, user=user, backend='django.contrib.auth.backends.ModelBackend')
        return redirect('main:index')


@login_required
def profile(request):
    # user = request.user
    # telegram_auth = UserSocialAuth.objects.filter(user=user, provider='telegram')[0]
    # telegram_id = telegram_auth.uid if telegram_auth else None
    return render(request, 'registration/profile.html')
    # return render(request, 'registration/profile.html', {'user_id': telegram_id})


@login_required
def edit_profile(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        bio = request.POST.get('bio')
        avatar = request.FILES.get('profile_image')
        profile_params = {'bio': bio,
                          'avatar': avatar}
    
        user_params = {'username': username,
                       'first_name': first_name,
                       'last_name': last_name,
                       'email': email,
                       'password': pwd}

        del_user_keys = []
        del_profile_keys = []

        profile = request.user.profile
        user = request.user

        for key in profile_params:
            if not profile_params[key]:
                del_profile_keys.append(key)

        for key in del_profile_keys:
            del profile_params[key]

        for key in user_params:
            if not user_params[key]:
                del_user_keys.append(key)

        for key in del_user_keys:
            del user_params[key]

        for key, value in user_params.items():
            if hasattr(user, key):
                setattr(user, key, value)

        for key, value in profile_params.items():
            if hasattr(profile, key):
                setattr(profile, key, value)

        user.save()
        profile.save()
        print(profile.avatar)
        return redirect('accounts:profile')
    return render(request, 'registration/edit_profile.html')


def guest_page(request, id):
    profile = get_object_or_404(Profile, id=id)
    return render(request, 'registration/guest_page.html', {'profile': profile})
