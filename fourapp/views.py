from django.shortcuts import render
from .models import Category, Post
from .functions import create_category
from .forms import PostForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

def crear_post(request):    
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'index.html')
    else:
        form = PostForm()
    return render(request, 'crear_post.html', {'form': form})