from django.contrib import admin
from .models import News, Category
from comments.models import Comment
# Register your models here.
class CommentInline(admin.TabularInline):
    model = Comment

class NewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'created', 'category', 'available']
    list_filter = ['author', 'created', 'updated', 'available', 'category']
    search_fields = ['title', 'author']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [CommentInline]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}


admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)