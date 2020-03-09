from django.shortcuts import render, redirect, reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from imagekit.models import ProcessedImageField
from annoying.decorators import ajax_request
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from . forms import UserCreateForm
from .models import UserProfile
from django.views.generic import (
    ListView, DetailView,
    CreateView, UpdateView, DeleteView
    )
from .models import Post
from django.contrib.auth.mixins import UserPassesTestMixin
from django.db.models import Q   

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

    return render(request, 'portfolio/register.html', {
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

    return render(request, 'portfolio/login.html', {
        'l_form': form
    })


def signout(request):
    logout(request)
    return redirect('home')


@login_required(login_url='/login/')
def home(request):
    return render(request, 'portfolio/home.html')

def profile(request):
    return render(request, 'portfolio/profile.html')
    

class view_post(DetailView):
    model = Post    

@login_required(login_url='/login/')
class create_post(CreateView):
    model = Post
    fields = ['caption', 'location']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@login_required(login_url='/login/')
class update_post(UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['caption']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

@login_required(login_url='/login/')
class DeletePost(UserPassesTestMixin, DeleteView):
    model = Post
    sucess_url = 'home'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


    def get_success_url(self):
        return reverse('home')


