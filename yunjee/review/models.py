from django.db import models
from writing.models import Blog
from login.models import Account
from django.contrib.auth.models import User

# Create your models here.
class Review(models.Model):
    blog = models.ForeignKey(Blog,on_delete = models.CASCADE, related_name='review')
    review_user = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
    review_body = models.TextField(blank = True)

    