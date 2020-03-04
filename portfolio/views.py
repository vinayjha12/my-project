from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from imagekit.models import ProcessedImageField
from annoying.decorators import ajax_request
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from . forms import UserCreateForm
from . models import UserProfile

# Create your views here.
def signup(request):
    form = UserCreateForm()

    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=request.POST['username'])
            profile = UserProfile(user=user)
            profile.save()

            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'])
            login(request, new_user)
            return redirect('login')

    return render(request, 'portfolio/signup.html', {
        's_form': form
    })


def login_user(request):
    form = AuthenticationForm()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('login')

    return render(request, 'portfolio/signup.html', {
        'l_form': form
    })


def signout(request):
    logout(request)
    return redirect('login')


def signup_success(request):
    return render(request, 'portfolio/signup_success.html')

@login_required(login_url='/login/')
def index(request):
    return render(request, 'libman/home.html')    