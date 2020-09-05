from django.db import models
from django.contrib.auth.models import User
from writing.models import Blog


# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    like_blog = models.ManyToManyField(Blog, blank=True, related_name='like_users')
    nickname = models.TextField(max_length="20")
    email = models.TextField(max_length=100)

