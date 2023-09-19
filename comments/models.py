from django.db import models
from main.models import News
from django.contrib.auth.models import User
# Create your models here.
class Comment(models.Model):
    author=models.ForeignKey(User, on_delete=models.CASCADE)
    text=models.TextField(max_length=300, verbose_name='Текст')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    news=models.ForeignKey(News, related_name='Комментарий', on_delete=models.CASCADE)
    parent=models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='answer', blank=True)

    def get_child_comments(self):
        return Comment.objects.filter(parent=self.id)