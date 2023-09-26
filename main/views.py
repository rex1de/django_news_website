from django.shortcuts import render, get_object_or_404, redirect
from slugify import slugify
from django.http import HttpResponse
from .models import News, Category
from accounts.models import Profile
from django.db.models import Q
from comments.models import Comment
from .subscribe_bot import *

# Create your views here.

def index(request):
    news=News.objects.filter(available=True)
    return render(request, 'main/index.html', {'news': news})

def news(request, id, slug):
    news = get_object_or_404(News, id=id, slug=slug, available=True)
    comments = Comment.objects.filter(news=news)
    news.post_views += 1
    news.save()
    return render(request, 'main/news.html', {'news': news,
                                              'comments': comments})
    
def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    news = News.objects.filter(category=category)
    return render(request, 'main/category.html', {'category': category,
                                                  'news': news})

def search(request):
    query = request.GET.get('q')
    news = News.objects.filter(Q(title__icontains=query) | Q(category__name=query) | Q(tags__name=query))
    return render(request, 'main/index.html', {'news': news})

def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        text = request.POST.get('text')
        id = request.POST.get('category')
        image = request.FILES.get('image')
        slug = slugify(title)
        category = get_object_or_404(Category, id=id)
        news = News(title=title, text=text, description=description, category=category, image=image, author=request.user, slug=slug)
        news.save()
        news_detail = {'title': news.title,
                'description': news.description,
                'image': news.image.url,
                'category': news.category.name,
                'url': news.get_absolute_url()}
        subscribed_users = Profile.objects.filter(subscription_categories=category)
        telegram_ids = []
        for i in subscribed_users:
            telegram_ids.append(subscribed_users.telegram) 
        send_to_subscribers(news_detail, telegram_ids)
        created_post(news_detail)
        return redirect(news)
    return render(request, 'main/create_post.html')
    
def like(request, id, slug):
    user = request.user
    news = get_object_or_404(News, id=id, slug=slug)
    likes = news.likes.all()
    dislikes = news.dislikes.all()
    if user in likes:
        news.likes.remove(user)
    elif user in dislikes:
        news.likes.add(user)
        news.dislikes.remove(user)
    else:
        news.likes.add(user)
    return redirect('main:news_detail', id=id, slug=slug)

def dislike(request, id, slug):
    user = request.user
    news = get_object_or_404(News, id=id, slug=slug)
    dislikes = news.dislikes.all()
    likes = news.likes.all()
    if user in dislikes:
        news.dislikes.remove(user)
    elif user in likes:
        news.dislikes.add(user)
        news.likes.remove(user)
    else:
        news.dislikes.add(user)
    return redirect('main:news_detail', id=id, slug=slug)
