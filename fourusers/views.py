from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import SignUpForm
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

def view_user(request):
    return

def settings(request):
    return