from django.db import models
from django.contrib.auth.models import User
from comments.models import Comment
from django.urls import reverse
from main.models import News

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True, upload_to='profile_images')
    bio = models.TextField()

    def __str__(self):
        return self.user.username
    
    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def get_absolute_url(self):
        return reverse('accounts:guest_page',
                       args=[self.id])     
    
    def get_user_comments(self):
        comments = Comment.objects.filter(author=self.user)
        return comments
    
    def get_user_news(self):
        news = News.objects.filter(author=self.user)
        return news