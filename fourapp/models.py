from asyncio.windows_events import NULL
from email.mime import image
from django.db import models

# Create your models here.

#Modelo de las categorías según las cuales se filtran
#lost posts
class Category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    short = models.CharField(max_length=3, null=False, default='sci')
    description = models.TextField(null=True)
    def __str__(self):
        return self.name

#modelo de los posts
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, null=False, blank=False, default='anon')
    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to='images/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=False, blank=False, default='anon')
    content = models.TextField(null=False, blank=False)
    reply_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content