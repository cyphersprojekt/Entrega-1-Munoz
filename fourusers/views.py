from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignUpForm
import fourapp.views
# Create your views here.


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(user)
            return redirect('fourapp:index')
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

def login(request):
    return

def logout(request):
    return

def view_user(request):
    return

def settings(request):
    return