from django.shortcuts import render
from .models import Category, Post
from .functions import create_category
from .forms import PostForm

# Create your views here.

def index(request):
    return render(request, 'index.html')