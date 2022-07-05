from django.shortcuts import redirect, render
from django.core.files.uploadedfile import InMemoryUploadedFile
from .models import Category, Post
from .forms import PostForm

# Create your views here.

def index(request):
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
        post = Post(username=username, title=title, content=content, image=image, category=Category.objects.get(categoryid=category))
        print(post)
        post.save()
        return redirect('/')

def view_category(request, category_id):
    category = Category.objects.get(categoryid=category_id)
    posts = Post.objects.filter(category=category).order_by('-post_id')
    return render(request, 'view_category.html', {'category': category, 'posts': posts})