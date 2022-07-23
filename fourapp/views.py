from django.shortcuts import redirect, render
from .models import Category, Post, Reply
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
#from .functions import clear_posts

# Create your views here.


def register(request):
    form = RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    return render(request, 'register.html', {'form': form})

def login(request):
    return render(request, 'login.html')

def index(request):
    #clear_posts()
    return render(request, 'index.html', {'categories': Category.objects.all()})

def image(request, image_id):
    image = Post.objects.get(post_id=image_id)
    return render(request, 'image.html', {'image': image})

def new_post(request):
    if request.method == 'POST':
        username = request.POST['username']
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST['category']
        # Por algún motivo que no comprendo, si la imagen está vacía
        # la poronga esta retorna un diccionario raro en lugar de NADA.
        # así que si eso sucede, piso el valor de 'image' para que no me rompa
        # las pelotas
        try:
            image = request.FILES['image']
        except:
            image = None
        post = Post(username=username, title=title, \
        content=content, image=image, \
        category=Category.objects.get(categoryid=category))
        print(post)
        post.save()
        return redirect('/')

def post_from_category(request, short):
    if request.method == 'POST':
        username = request.POST['username']
        title = request.POST['title']
        content = request.POST['content']
        category = Category.objects.get(short=short)
        try:
            image = request.FILES['image']
        except:
            image = None
        post = Post(username=username, title=title, \
        content=content, image=image, \
        category=category)
        post.save()
        return redirect(f'/{short}')
    else:
        return render(request, 'post_from_category.html', {'category': Category.objects.get(short=short)})

def reply(request, post_id):
    if request.method == 'POST':
        username = request.POST['username']
        content = request.POST['content']
        try:
            image = request.FILES['image']
        except:
            image = None
        post = Post.objects.get(post_id=post_id)
        reply = Reply(username=username, content=content, image=image, post=post)
        reply.save()
        return redirect(f'/post/{post_id}')

def view_category_by_id(request, category_id):
    category = Category.objects.get(categoryid=category_id)
    categories = Category.objects.all()
    posts = Post.objects.filter(category=category).order_by('-post_id')
    return render(request, 'view_category.html', {'category': category, 'posts': posts, 'categories': categories})

def view_category_by_short(request, short):
    category = Category.objects.get(short=short)
    categories = Category.objects.all()
    posts = Post.objects.filter(category=category).order_by('-post_id')
    return render(request, 'view_category.html', {'category': category, 'posts': posts, 'categories': categories})

def view_post(request, post_id):
    categories = Category.objects.all()
    category = Post.objects.get(post_id=post_id).category
    post = Post.objects.get(post_id=post_id)
    replies = Reply.objects.filter(post=post).order_by('-reply_id')
    return render(request, 'view_post.html', {'post': post, 'replies': replies, 'categories': categories, 'category': category})