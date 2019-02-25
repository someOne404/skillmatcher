from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
# from .models import Post

from django.contrib.auth.models import User
from .filters import UserFilter

from django.contrib.auth import get_user_model
User = get_user_model()

def home(request):
    template_name = './social_match/base.html'

    if 'change_status' in request.POST:
        current_user = request.user
        current_user.status_active = not current_user.status_active
        current_user.save()

    user_list = User.objects.filter(status_active=True, is_superuser=False)
    context = {'user_list': user_list}
    return render(request, template_name, context)
    

def index(request):
    template_name = './social_match/index.html'

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
    return render(request, './social_match/user_list.html', {'filter': user_filter})

