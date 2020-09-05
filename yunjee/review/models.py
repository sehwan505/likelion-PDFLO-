from django.db import models

# Create your models here.
class Review(models.Model):
    review_rating = models.TextField()
    review_content = models.TextField()


    

