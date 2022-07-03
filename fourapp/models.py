from asyncio.windows_events import NULL
from email.mime import image
from django.db import models

# Create your models here.

class Category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    def __str__(self):
        return self.name

class Post(models.Model):
    postid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, null=True)
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/', blank=True)
    def __str__(self):
        return self.title