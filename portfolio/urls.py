from django.conf.urls import url

from . import views

urlpatterns = [
    url('', views.home, name='home'),
    url('profile/', views.profile, name='profile'),
    url('register/', views.signup, name='signup'),
    url('login/', views.login_user, name='login'),
    url('signout/', views.signout, name='signout'),
    url('post/', views.view_post, name='signout'),
    url('createpost/', views.create_post, name='create_post'),
    url('updatepost/', views.update_post, name='update_post'),
]    