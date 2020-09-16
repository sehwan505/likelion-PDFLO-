from django.db import models
from django.contrib.auth.models import User
from writing.models import Blog
from django.dispatch import receiver
from django.db.models.signals import post_save



# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    like_blog = models.ManyToManyField(Blog, blank=True, related_name='like_users')
    nickname = models.TextField(max_length="20")
    introduction = models.TextField(max_length="100", blank=True)
    email = models.TextField(max_length=100)

    profile_photo = models.ImageField(blank=True, default="image/elly.png", upload_to="image/profile")
    user_purchase_list = models.ManyToManyField(Blog, blank=True, related_name='user_purchase_list')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Account.objects.create(user=instance)