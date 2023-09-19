from django.db.models.signals import post_save
from .models import Category, Tag
from django.dispatch import receiver

@receiver(post_save, sender=Category)
def create_tag(sender, instance, created, **kwargs):
    if created:
        Tag.objects.create(name=instance.name.lower())


@receiver(post_save, sender=Category)
def save_tag(sender, instance, **kwargs):
    try:
        Tag.objects.get(name=instance.name.lower()).save()
    except:
        pass