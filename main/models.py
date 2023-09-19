from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='child_category', blank=True)

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def get_absolute_url(self): 
        return reverse('news:category',
                       args=[self.slug])     

    def get_child_categories(self):
        return Category.objects.filter(parent=self.id)
    
class Tag(models.Model):
    name = models.CharField(max_length=25, verbose_name='Название')

    def __str__(self):
        return self.name
        
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

class News(models.Model):
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    text = models.TextField(max_length=300, verbose_name='Текст')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    description = models.TextField(max_length=100, null=True, verbose_name='Описание')
    image = models.ImageField(upload_to='news_images/', verbose_name='Изображение')
    slug = models.SlugField(max_length=50, unique=True, verbose_name='Слаг')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    available = models.BooleanField(default=True, verbose_name='Доступно для просмотра')
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name='Категория')   
    likes = models.ManyToManyField(User, verbose_name='Лайки', related_name='likes', blank=True)
    dislikes = models.ManyToManyField(User, verbose_name='Дизлайки', related_name='dislikes', blank=True)
    post_views = models.PositiveIntegerField(verbose_name='Просмотры', default=0)
    tags = models.ManyToManyField(Tag, verbose_name='Теги', related_name='Tags')
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('news:news_detail',
                       args=[self.id, self.slug])        
    class Meta:
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'

