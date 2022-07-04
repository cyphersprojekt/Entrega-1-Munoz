from django.shortcuts import render
from .models import Category, Post

# Create your views here.

def index(request):
    return render(request, 'index.html')

def image(request, image_id):
    image = Post.objects.get(post_id=image_id)
    return render(request, 'image.html', {'image': image})