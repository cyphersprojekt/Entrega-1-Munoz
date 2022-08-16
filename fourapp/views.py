from django.shortcuts import redirect, render
from .models import Category, Post, Reply
from .forms import RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required


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
    if not Category.objects.filter(short='gen').exists():
        Category.objects.create(categoryid=1, name='General', short='gen', description='General discussion', nsfw=False)
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
        else:
            registered_user = None
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
        else:
            registered_user = None
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
        else:
            registered_user = None
        post = Post.objects.get(post_id=post_id)
        reply = Reply(registereduser=registered_user, username=username, \
                    content=content, image=image, post=post)
        reply.save()
        return redirect(f'/post/{post_id}')

def view_category_by_id(request, category_id):
    category = Category.objects.get(categoryid=category_id)
    categories = Category.objects.all()
    posts = Post.objects.filter(category=category).order_by('-post_id')
    context = {'category': category, 'posts': posts, 'categories': categories}
    return render(request, 'view_category.html', context)

def view_category_by_short(request, short):
    category = Category.objects.get(short=short)
    categories = Category.objects.all()
    posts = Post.objects.filter(category=category).order_by('-post_id')
    if category.nsfw == True:
        if request.user.is_authenticated:
            return render(request, 'view_category.html', {'category': category, 'posts': posts, 'categories': categories})
        else:
            return redirect('/login/')
    else:
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
        deletable = True
    else:
        editable = False
        deletable = False

    context = {'post': post, 'replies': replies, 'category': category, 'categories': categories, 'replycounter': replycounter, 'editable': editable, 'deletable': deletable}
    return render(request, 'view_post.html', context)

@login_required(login_url='/login/')
def edit_post(request, post_id):
    post = Post.objects.get(post_id=post_id)
    if request.method == 'POST':
        if post.registereduser == request.user:
            post.title = request.POST['title']
            post.content = request.POST['content']
            try:
                post.image = request.FILES['image']
            except:
                post.image = None
            post.edited = True
            post.save()
            return redirect(f'/post/{post_id}')
        else:
            messages.error(request, 'You are not the owner of this post')
            return redirect(f'/post/{post_id}')
    else:
        return render(request, 'edit_post.html', {'post': post})

@login_required(login_url='/login/')
def delete_post(request, post_id):
    post = Post.objects.get(post_id=post_id)
    replies = Reply.objects.filter(post=post)
    if request.method == 'POST':
        if post.registereduser == request.user:
            replies.delete()
            post.delete()
            return redirect('/')
        else:
            messages.error(request, 'You are not the owner of this post')
            return redirect(f'/post/{post_id}')
    else:
        return render(request, 'delete_post.html', {'post': post})

def about(request):
    categories = Category.objects.all()
    return render(request, 'about.html', {'categories': categories})

@login_required(login_url='/login/')
def view_user(request):
    user = request.user
    posts = Post.objects.filter(registereduser=user).order_by('-post_id')
    return render(request, 'view_user.html', {'user': user, 'posts': posts, 'categories': Category.objects.all()})

@login_required(login_url='/login/')
def settings(request):
    user = request.user
    if request.method == 'GET':
        return render(request, 'settings.html', {'user': user, 'categories': Category.objects.all()})

    def change_username(request):
        user = request.user
        if request.POST['username'] != '':
            if request.POST['username'] != user.username:
                if check_password(request.POST['password'], user.password):
                    user.username = request.POST['username']
                    user.save()
                    messages.success(request, 'Username changed')
                    return redirect('/user/settings')
                else:
                    messages.error(request, 'Wrong password when changing username')
                    return redirect('/user/settings')
            else:
                messages.error(request, 'Can\'t change to the same username')
                return redirect('/user/settings')
        else:
            messages.error(request, 'Username can\'t be empty')
            return redirect('/user/settings')

    def change_password(request):
        user = request.user
        if request.POST.get('new_password') != '':
            if check_password(request.POST.get('oldpassword'), user.password):
                if request.POST.get('newpassword1') == request.POST.get('newpassword2'):
                    user.password = make_password(request.POST.get('newpassword1'))
                    user.save()
                    messages.success(request, 'Password changed')
                    return redirect('/user/settings')
                else:
                    messages.error(request, 'Passwords don\'t match')
                    return redirect('/user/settings')
            else:
                messages.error(request, 'Wrong password when changing password')
                return redirect('/user/settings')
        else:
            messages.error(request, 'Password can\'t be empty')
            return redirect('/user/settings')

    def delete_posts(request):
        user = request.user
        if request.method == 'POST':
            if check_password(request.POST.get('password'), user.password):
                post = Post.objects.filter(registereduser=user).all()
                post.delete()
                messages.success(request, 'All posts deleted')
                return redirect('/user/settings')
            else:
                messages.error(request, 'Wrong password when deleting posts')
                return redirect('/user/settings')
        else:
            return redirect('/user/settings')

    def delete_account(request):
        user = request.user
        if request.method == 'POST':
            if check_password(request.POST.get('password'), user.password):
                user.delete()
                messages.success(request, 'Account deleted')
                return redirect('/')
            else:
                messages.error(request, 'Wrong password')
                return redirect('/user/settings')
        else:
            return redirect('/user/settings')

    if request.POST['form_type'] == 'change_username':
        return change_username(request)
    elif request.POST['form_type'] == 'change_password':
        return change_password(request)
    elif request.POST['form_type'] == 'delete_posts':
        return delete_posts(request)
    elif request.POST['form_type'] == 'delete_account':
        return delete_account(request)
    else:
        return redirect('/user/settings')

def search(request):
    categories = Category.objects.all()
    if request.method == 'GET':
        return render(request, 'search.html', {'categories': categories})
    else:
        search_query = request.POST['search_query']
        titles = Post.objects.filter(title__icontains=search_query)
        contents = Post.objects.filter(content__icontains=search_query)
        usernames = Post.objects.filter(username__icontains=search_query)
        posts = titles | contents | usernames
        return render(request, 'search.html', {'posts': posts, 'categories': categories, 'search_query': search_query})