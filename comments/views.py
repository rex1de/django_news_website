from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Comment
from main.models import News
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


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
        parent_id = request.POST.get('related_comment')
        if parent_id:
            related_comment = Comment.objects.get(id=parent_id)
            comment = Comment(author=request.user, text=text, news=news, parent=related_comment)
        else: 
            comment = Comment(author=request.user, text=text, news=news)

        comment.save()
    return redirect('main:news_detail', id=id, slug=slug)