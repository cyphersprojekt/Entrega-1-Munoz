from django.shortcuts import render
from .models import Category, Post
from .functions import create_category

# Create your views here.

def index(request):
    return render(request, 'index.html')

def crear_post(request):    
    p_username = request.POST.get('username')
    p_title = request.POST.get('title')
    p_content = request.POST.get('content')
    p_category = request.POST.get('category')
    p_image = request.FILES.get('image')

    post = Post(username=p_username, \
                title=p_title, \
                content=p_content, \
                category=Category(p_category), \
                image=p_image)
    post.save()
    return render(request, 'index.html')