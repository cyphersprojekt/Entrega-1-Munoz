from django.shortcuts import redirect, render
from .models import Category, Post, Reply
from .forms import RegisterForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from .functions import clear_posts

# Create your views here.


def register_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        form = RegisterForm()
        if request.method == 'POST':
            form = RegisterForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'User successfully created!')
                return redirect('login')
        return render(request, 'register.html', {'form': form})

def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, \
                                        password=password)
            if user != None:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('login')
        return render(request, 'login.html')

def logout_page(request):
    logout(request)
    return redirect('/')

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
        if request.user.is_authenticated:
            registered_user = request.user
        post = Post(registereduser=registered_user, username=username, title=title, \
                    content=content, image=image, \
                    category=Category.objects.get(categoryid=category))
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
        if request.user.is_authenticated:
            registered_user = request.user
        post = Post(registereduser=registered_user, username=username, title=title, \
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
        if request.user.is_authenticated:
            registered_user = request.user
        post = Post.objects.get(post_id=post_id)
        reply = Reply(registereduser=registered_user, username=username, \
                    content=content, image=image, post=post)
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
    replycounter = Reply.objects.filter(post_id=post_id).count()
    post.viewcounter = post.viewcounter + 1
    post.save()
    if request.user == post.registereduser:
        editable = True
    else:
        editable = False
    return render(request, 'view_post.html', {'post': post, 'replies': replies, 'categories': categories, 'category': category, 'editable': editable, 'replycounter': replycounter, 'viewcounter': post.viewcounter, 'replycounter': replycounter})

@login_required(login_url='/login/')
def edit_post(request, post_id):
    post = Post.objects.get(post_id=post_id)
    if request.method == 'POST':
        if post.registereduser == request.user:
            post.title = request.POST['title']
            post.content = request.POST['content']
            post.image = request.FILES['image']
            post.edited = True
            post.save()
            return redirect(f'/post/{post_id}')
        else:
            messages.error(request, 'You are not the owner of this post')
            return redirect(f'/post/{post_id}')
    else:
        return render(request, 'edit_post.html', {'post': post})