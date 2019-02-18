from django.urls import path

from . import views

app_name = 'social_match'
urlpatterns = [
    path('', views.index, name='index'),
]