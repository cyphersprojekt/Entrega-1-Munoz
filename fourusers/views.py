from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.views.generic import DetailView
from django.contrib import messages
from .forms import SignUpForm
from .models import Profile
from fourapp.models import Post, Category
from django.contrib.auth.decorators import login_required
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

    # cuando el usuario se registra, yo no tengo idea cual es el id que se le asigna.
    # (seguramente este en algun return, no lo busque). en SQL podrias hacer un trigger
    # after insert para que el perfil se genere automaticamente una vez que se inserta un
    # usuario, pero si lo quiero hacer solo en python, y dado que la pantalla de registro
    # te redirecciona al login, lo que hago es chequear si NO existe el perfil una vez que
    # inicio sesion, y solo en ese caso disparar la creacion del objeto.

    if request.user.is_authenticated:
        if not Profile.objects.filter(user=request.user).exists():
            Profile.objects.create(user=request.user, name=request.user.username)
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



# va a funcionar siempre y cuando los usuarios se generen a traves del register
# porque lo que triggerea la creacion del perfil es el redirect a index.
# si se crea un usuario a traves de la consola, o del panel de administrador
# lo primero que hay que hacer es iniciar sesion desde la web, porque sino
# explota todo

class ProfilePage(DetailView):
    model = Profile
    template_name = 'profile.html'
    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        puser = get_object_or_404(Profile, id=self.kwargs['pk'])
        context = super(ProfilePage, self).get_context_data(*args, **kwargs)
        context['pagetitle'] = f'4jango - {puser.name}'
        context['categories'] = Category.objects.all()
        context['puser'] = puser
        context['posts'] = Post.objects.filter(registereduser=puser.user_id).all()
        return context