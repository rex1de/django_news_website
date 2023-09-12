from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import News, Category
from comments.models import Comment
# Create your views here.
def index(request):
    news=News.objects.filter(available=True)
    return render(request, 'main/index.html', {'news': news})

def news(request, id, slug):
    news = get_object_or_404(News, id=id, slug=slug, available=True)
    comments = Comment.objects.filter(news=news)
    return render(request, 'main/news.html', {'news': news,
                                              'comments': comments})

def category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    news = News.objects.filter(category=category)
    return render(request, 'main/category.html', {'category': category,
                                                  'news': news})

def search(request):
    query = request.GET.get('q')
    news = News.objects.filter(title__icontains=query)
    return render(request, 'main/index.html', {'news': news})