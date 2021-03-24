from django.db import models
from django.urls import reverse


# Create your models here.
class Blog(models.Model):
    title = models.CharField(max_length = 200)
    money = models.CharField(max_length = 200)
    one_line = models.CharField(max_length = 200)
    page = models.IntegerField(default = 0)
    category = models.CharField(default="실무", max_length=20)
    image = models.ImageField(null = True, blank = True, upload_to = 'image', default="image/elly.png")
    pub_date=models.DateTimeField(auto_now_add=True)
    seller = models.TextField()
    seller_comment = models.TextField(default="")
    seller_num = models.TextField(max_length=12, default=0)
    seller_spec = models.TextField(default = "")
    seller_story = models.TextField(default = "")
    pdf_subject1 = models.TextField(default="")
    pdf_subject2 = models.TextField(default="")
    pdf_why1 = models.TextField(default="")
    pdf_why2 = models.TextField(default="")
    pdf_spec1 = models.TextField(default="")
    pdf_spec2 = models.TextField(default="")
    content = models.TextField()
    content_list = models.TextField(default="")
    count = models.IntegerField(default=0)
    like_num = models.PositiveIntegerField(default=0, blank=True)


    def summary(self):
        return self.body[:100]

    def get_url(self):
        return reverse('detail', args=[self.id])



    