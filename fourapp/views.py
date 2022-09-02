from multiprocessing import context
from django.shortcuts import redirect, render
from .models import Category, Post, Reply
from .forms import RegisterForm, PostFormIndex, PostFormCategory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from fourusers.models import Profile


def index(request):
    form = PostFormIndex()
    pagetitle = '4jango - Home'
    categories = Category.objects.all()
    context = {'categories': categories, 'pagetitle': pagetitle, 'form': form}
    if not Category.objects.filter(categoryid=1).exists():
        Category.objects.create(categoryid=1, name='General', short='gen', description='General discussion', nsfw=False)
    if request.user.is_authenticated:
        if not Profile.objects.filter(user=request.user).exists():
            Profile.objects.create(user=request.user, name=request.user.username)
    return render(request, 'index.html', context)


def image(request, image_id):
    image = Post.objects.get(post_id=image_id)
    pagetitle = f'4jango - Image {image_id}'
    return render(request, 'image.html', {'image': image, 'pagetitle': pagetitle}) 

def new_post(request):
    if request.method == 'POST':
        username = request.POST['username']
        title = request.POST['title']
        content = request.POST['content']
        category = request.POST.get('category')
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
    category = Category.objects.get(short=short)
    categories = Category.objects.all()
    pagetitle = f'4jango - New post in {category.name}'
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
        return render(request, 'post_from_category.html', {'category': category, 'categories': categories, 'pagetitle': pagetitle})

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
    form = PostFormCategory()
    category = Category.objects.get(categoryid=category_id)
    categories = Category.objects.all()
    posts = Post.objects.filter(category=category).order_by('-post_id')
    pagetitle = f'4jango - {category.name}'
    context = {'category': category, 'posts': posts, 'categories': categories, 'pagetitle': pagetitle, 'form': form}
    if category.nsfw == True:
        if request.user.is_authenticated:
            return render(request, 'view_category.html', context)
        else:
            return redirect('/login/')
    return render(request, 'view_category.html', context)

def view_category_by_short(request, short):
    form = PostFormCategory()
    category = Category.objects.get(short=short)
    categories = Category.objects.all()
    posts = Post.objects.filter(category=category).order_by('-post_id')
    pagetitle = f'4jango - {category.name}'
    context = {'category': category, 'posts': posts, 'categories': categories, 'pagetitle': pagetitle, 'form': form}
    if category.nsfw == True:
        if request.user.is_authenticated:
            return render(request, 'view_category.html', context)
        else:
            return redirect('/login/')
    else:
        return render(request, 'view_category.html', context)

def view_post(request, post_id):
    pagetitle = f'4jango - Post #{post_id}'
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

    context = {'post': post, 'replies': replies, 'category': category, 'categories': categories, 'replycounter': replycounter, 'editable': editable, 'deletable': deletable, 'pagetitle': pagetitle}
    return render(request, 'view_post.html', context)

@login_required(login_url='/login/')
def edit_post(request, post_id):
    post = Post.objects.get(post_id=post_id)
    categories = Category.objects.all()
    pagetitle = f'4jango - Edit post #{post_id}'
    context = {'post': post, 'categories': categories, 'pagetitle': pagetitle}
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
        return render(request, 'edit_post.html', context)

@login_required(login_url='/login/')
def delete_post(request, post_id):
    categories = Category.objects.all()
    post = Post.objects.get(post_id=post_id)
    replies = Reply.objects.filter(post=post)
    pagetitle = f'4jango - Delete post #{post_id}'
    context = {'post': post, 'replies': replies, 'pagetitle': pagetitle, 'categories': categories}
    if request.method == 'POST':
        if post.registereduser == request.user:
            replies.delete()
            post.delete()
            return redirect('/')
        else:
            messages.error(request, 'You are not the owner of this post')
            return redirect(f'/post/{post_id}')
    else:
        return render(request, 'delete_post.html', context)

class AboutView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['pagetitle'] = '4jango - About'
        return context
    template_name = 'about.html'    

def search(request):
    categories = Category.objects.all()
    pagetitle = '4jango - Search'
    context = {'categories': categories, 'pagetitle': pagetitle}
    if request.method == 'GET':
        return render(request, 'search.html', context)
    else:
        search_query = request.POST['search_query']
        titles = Post.objects.filter(title__icontains=search_query)
        contents = Post.objects.filter(content__icontains=search_query)
        usernames = Post.objects.filter(username__icontains=search_query)
        posts = titles | contents | usernames
        context = {'categories': categories, 'pagetitle': pagetitle, 'posts': posts}
        return render(request, 'search.html', context)