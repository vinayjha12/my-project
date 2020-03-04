from django.conf.urls import url

from . import views

urlpatterns = [
    url('signup/', views.signup, name='signup'),
    url('login/', views.login_user, name='login'),
    url('signout/', views.signout, name='signout'),
    url('signup_success/', views.signup_success, name='signup_success'),
] 