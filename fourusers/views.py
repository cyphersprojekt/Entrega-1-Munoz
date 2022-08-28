from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import SignUpForm, UserProfileForm
from .models import UserProfile
from fourapp.models import Post, Category

# Create your views here.


def register(request):
    if request.user.is_authenticated:
        return redirect('fourapp:index')
    else:
        form = SignUpForm()
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'User successfully created!')
                UserProfile.objects.create(username=form.cleaned_data['username'])
                return redirect('fourusers:login')
        return render(request, 'register.html', {'form': form})

def login_user(request):
    if request.user.is_authenticated:
        return redirect('fourapp:index')
    else:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user != None:
                login(request, user)
                return redirect('fourapp:index')
            else:
                messages.error(request, 'Invalid username or password')
                return redirect('fourusers:login')
        return render(request, 'login.html')

def log_out(request):
    logout(request)
    return redirect('fourapp:index')


# TODO: Ver si puedo juntar my_profile con view_user para no tener dos funciones separadas innecesariamente
def my_profile(request):
    if not request.user.is_authenticated:
        return redirect('fourapp:index')
    else:
        profile = UserProfile.objects.get(username=request.user.username)
        posts = Post.objects.filter(registereduser=request.user).order_by('-post_id')
        pagetitle = f'4jango - {profile.username}\'s profile'
        context = {'posts': posts, 'profile': profile, 'pagetitle': pagetitle}
        return render(request, 'profile.html', context)

def view_user(request, username):
    return redirect('http://www.google.com')


# TODO: Armar el manejo del POST de settings
@login_required(login_url='/login/')
def settings(request):
    form = UserProfileForm
    return render(request, 'settings.html', {'form': form})