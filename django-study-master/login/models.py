from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    nickname = models.TextField(max_length="20")
    email = models.TextField(max_length=100)