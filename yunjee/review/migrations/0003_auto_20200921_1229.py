# Generated by Django 3.1 on 2020-09-21 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_auto_20200911_1348'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='review_body',
            field=models.TextField(max_length=200),
        ),
    ]
