from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Comment
from main.models import News
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


@login_required
def post_comment(request, id, slug):
    news = get_object_or_404(News, id=id, slug=slug)
    if request.method == 'POST':
        text = request.POST.get('comment_text')
        comment = Comment(author=request.user, text=text, news=news)
        comment.save()
    return redirect('main:news_detail', id=id, slug=slug)