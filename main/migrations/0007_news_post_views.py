# Generated by Django 4.2.4 on 2023-09-14 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_news_dislikes_news_likes'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='post_views',
            field=models.PositiveIntegerField(null=True, verbose_name='Просмотры'),
        ),
    ]
