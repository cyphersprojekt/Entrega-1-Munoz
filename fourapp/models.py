from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.

#Modelo de las categorías según las cuales se filtran
#lost posts
class Category(models.Model):
    categoryid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=False)
    short = models.CharField(max_length=3, null=False, default='aaa', unique=True)
    description = models.TextField(null=True)
    nsfw = models.BooleanField(default=False)
    def __str__(self):
        return self.name

#modelo de los posts
class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=255, null=False, blank=False, default='anon')
    registereduser = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=255, null=False)
    #content = models.TextField(null=False, blank=False)
    content = RichTextField(null=False, blank=False)
    image = models.ImageField(upload_to='postimgs/', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    edited = models.BooleanField(default=False)
    viewcounter = models.IntegerField(default=0)
    post_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

class Reply(models.Model):
    reply_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, null=False, blank=False, default='anon')
    registereduser = models.ForeignKey('auth.User', related_name='replies', on_delete=models.CASCADE, null=True)
    content = models.TextField(null=False, blank=False)
    image = models.ImageField(upload_to='replyimgs/', null=True, blank=True)
    edited = models.BooleanField(default=False)
    reply_date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.content