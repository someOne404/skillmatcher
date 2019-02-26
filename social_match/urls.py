from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'social_match'
urlpatterns = [
    path('', views.base, name='base'),
    path('about/', views.about, name='about'),
    path('home/', views.home, name='home'),
    path('search/', views.search, name='search'),
    path('createpost/', views.createpost, name='createpost'),
    path('profile/', views.profile, name='profile'),
    path('posts/', views.posts, name='posts'),
]