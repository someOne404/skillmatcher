from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
# from .models import Post

from django.contrib.auth.models import User
from .filters import UserFilter
from .forms import PostForm

from django.contrib.auth import get_user_model
User = get_user_model()

def base(request):
    template_name = './social_match/base.html'
    return render(request, template_name)

def about(request):
    template_name = './social_match/about.html'
    return render(request, template_name)

def home(request):
    template_name = './social_match/home.html'

    if 'change_status' in request.POST:
        current_user = request.user
        current_user.status_active = not current_user.status_active
        current_user.save()

    user_list = User.objects.filter(status_active=True, is_superuser=False)
    context = {'user_list': user_list}
    return render(request, template_name, context)

def search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, './social_match/search.html', {'filter': user_filter})

def createpost(request):
    template_name = './social_match/createpost.html'
    form = PostForm()
    return render(request,template_name, {'form': form})

def profile(request):
    template_name = './social_match/profile.html'

    if 'change_status' in request.POST:
        current_user = request.user
        current_user.status_active = not current_user.status_active
        current_user.save()

    return render(request,template_name)

def posts(request):
    template_name = './social_match/posts.html'    
    return render(request,template_name)

