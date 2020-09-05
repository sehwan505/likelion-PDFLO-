from django.db import models
from django.urls import reverse


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length = 200)
    money = models.CharField(max_length = 200)
    one_line = models.CharField(max_length = 200)
    image = models.ImageField(null = True, blank = True, upload_to = 'image', default="image/elly.png")
    pub_date=models.DateTimeField(auto_now_add=True)
    seller = models.TextField()
    content = models.TextField()
    content_list = models.TextField()
    count = models.IntegerField(default = 0)
    like_num = models.PositiveIntegerField(default=0, blank=True)

    def __str__(self):
        return self.name

    def summary(self):
        return self.body[:100]

    def get_url(self):
        return reverse('detail', args=[self.id])



    


    