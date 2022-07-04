from django.shortcuts import redirect, render
from .models import Category, Post
from .forms import PostForm

# Create your views here.

def index(request):
    return render(request, 'index.html')

def image(request, image_id):
    image = Post.objects.get(post_id=image_id)
    return render(request, 'image.html', {'image': image})

def new_post(request):
    if request.method == 'POST':
        username = request.POST['username']
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES['image']
        category = request.POST['category']
        post = Post(username=username, title=title, content=content, image=image, category=Category.objects.get(categoryid=category))
        post.save()
        return redirect('index')

def view_category(request, category_id):
    category = Category.objects.get(categoryid=category_id)
    posts = Post.objects.filter(category=category).order_by('-post_id')
    return render(request, 'view_category.html', {'category': category, 'posts': posts})