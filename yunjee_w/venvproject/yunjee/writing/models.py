from django.db import models


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length = 200)
    money = models.CharField(max_length = 200)
    one_line = models.CharField(max_length = 200)
    image = models.ImageField(null = True, blank = True, upload_to = 'image')
    seller = models.TextField()
    content = models.TextField()
    content_list = models.TextField()
    
    
    
    def __str__(self):
        return self.name




    


    