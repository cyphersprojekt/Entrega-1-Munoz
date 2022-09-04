from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.views.generic import DetailView
from django.contrib.auth.hashers import check_password, make_password
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

@login_required(login_url='/users/login/')
def log_out(request):
    logout(request)
    return redirect('fourapp:index')

class ProfilePage(DetailView):
    
    # va a funcionar siempre y cuando los usuarios se generen a traves del register
    # porque lo que triggerea la creacion del perfil es el redirect a index.
    # si se crea un usuario a traves de la consola, o del panel de administrador
    # lo primero que hay que hacer es iniciar sesion desde la web, porque sino
    # explota todo

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


@login_required(login_url='/users/login/')
def settings(request):
    user = request.user
    profile = Profile.objects.get(pk=user.pk)
    pagetitle = f'4jango - Settings'
    categories = Category.objects.all()
    context = {'user': user, 'profile': profile, 'pagetitle': pagetitle, 'categories': categories}

    if request.method == 'GET':
        return render(request, 'settings.html', context)

    def change_name(request):
        if request.POST['new_name'] != '':
            if request.POST['new_name'] != user.profile.name:
                user.profile.name = request.POST['new_name']
                user.profile.save()
                messages.success(request,'Profile name successfully updated')
            else:
                messages.error(request, 'Your new name cannot be the same as the old one!')
        else:
            messages.error(request, 'Your new name cannot be empty!')
        return redirect('fourusers:settings')
    
    def change_bio(request):
        if request.POST['new_bio'] != user.profile.bio:
            user.profile.bio = request.POST['new_bio']
            user.profile.save()
            messages.success(request,'Profile bio successfully updated')
        else:
            messages.error(request, 'Your new bio cannot be the same as the old one!')
        return redirect('fourusers:settings')

    def change_picture(request):
        if request.FILES['new_picture'] != user.profile.picture:
            try:
                user.profile.picture = request.FILES['new_picture']
                user.profile.save()
            except:
                messages.error(request, 'There was an error on our side, your profile picture couldn\'t be changed')
        else:
            messages.error(request, 'It seems like your new profile picture is the same as the old one...')
        return redirect('fourusers:settings')
    
    def change_link(request):
        if request.POST['new_link'] != user.profile.link:
            user.profile.link = request.POST['new_link']
            user.profile.save()
        else:
            messages.error(request, 'It seems like your new external link is the same as the old one...')
        return redirect('fourusers:settings')
    
    def change_password(request):
        user = request.user
        if request.POST.get('new_password') != '':
            if check_password(request.POST.get('oldpassword'), user.password):
                if request.POST.get('newpassword1') == request.POST.get('newpassword2'):
                    user.password = make_password(request.POST.get('newpassword1'))
                    user.save()
                    messages.success(request, 'Password changed, log back in')
                    return redirect('fourusers:settings')
                else:
                    messages.error(request, 'Passwords don\'t match')
                    return redirect('fourusers:settings')
            else:
                messages.error(request, 'Wrong password when changing password')
                return redirect('fourusers:settings')
        else:
            messages.error(request, 'Password can\'t be empty')
            return redirect('fourusers:settings')

    if request.POST['form_type'] == 'change_password':
        return change_password(request)
    elif request.POST['form_type'] == 'change_link':
        return change_link(request)
    elif request.POST['form_type'] == 'change_picture':
        return change_picture(request)
    elif request.POST['form_type'] == 'change_bio':
        return change_bio(request)
    elif request.POST['form_type'] == 'change_name':
        return change_name(request)
    else:
        return redirect('fourusers:settings')