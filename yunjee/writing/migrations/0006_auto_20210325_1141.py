# Generated by Django 3.1 on 2021-03-25 02:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('writing', '0005_blog_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='filename',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='blog',
            name='filesize',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='blog',
            name='preview',
            field=models.ImageField(blank=True, default='image/elly.png', null=True, upload_to='image'),
        ),
    ]
