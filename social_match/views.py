from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from .models import Post

from django.contrib.auth.models import User
from .filters import UserFilter
from .forms import PostForm, ProfileForm

from django.contrib.auth import get_user_model
import datetime

User = get_user_model()

def base(request):
    template_name = './social_match/base.html'
    return render(request, template_name)

def about(request):
    template_name = './social_match/about.html'
    return render(request, template_name)

def home(request):
    template_name = './social_match/home.html'
    user_list = User.objects.filter(status_active=True, is_superuser=False)
    post_list = Post.objects.all()

    context = {'user_list': user_list, 'post_list':post_list}
    return render(request, template_name, context)

def search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, './social_match/search.html', {'filter': user_filter})

def createpost(request):
    template_name = './social_match/createpost.html'
    form = PostForm()

    if request.method == 'POST':
       form = PostForm(request.POST)
       if form.is_valid():
           post = form.save(commit=False)
           post.user = request.user
           post.save()

           headline = form.cleaned_data["headline"]
           message = form.cleaned_data["message"]
           p = Post(headline = headline, message=message, user=request.user, date=datetime.datetime.now())
           p.save()

           form = PostForm()
           
    else:
        form = PostForm()

    return render(request,template_name, {'form': form})

def profile(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('social_match:home'))

    if 'change_status' in request.POST:
        current_user = request.user
        current_user.status_active = not current_user.status_active
        current_user.save()

    template_name = './social_match/profile.html'
    user = request.user
    form = ProfileForm(initial={
        'first_name': user.first_name,
        'last_name': user.last_name,
        'phone': user.phone,
        'class_standing': user.class_standing,
        'graduation_year': user.graduation_year,
        'majors': user.majors,
        'minors': user.minors,
        'courses': user.courses,
        'interests': user.interests,
        'skills': user.skills,
        'activities': user.activities,
    })

    return render(request, template_name, {'user': user, 'form': ProfileForm})    

def myposts(request):
    template_name = './social_match/myposts.html'
    return render(request, template_name)



