from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone

from .models import Post
from .filters import UserFilter
from .forms import PostForm, ProfileForm, EditPostForm

from datetime import datetime
import math

User = get_user_model()

def base(request):
    template_name = './social_match/base.html'
    return render(request, template_name)

def about(request):
    template_name = './social_match/about.html'
    return render(request, template_name)

def home(request):
    posts_per_page = 20
    template_name = './social_match/home.html'
    user_list = User.objects.filter(status_active=True, is_superuser=False)
    max_sets = math.ceil(len(Post.objects.filter(
        date__lte=timezone.now(),
        post_active=True
    )) / posts_per_page)

    if 'newer' in request.POST:
        post_set = int(request.POST.get("current_set")) - 1
        post_list = Post.objects.filter(
            date__lte=timezone.now(),
            post_active=True
        ).order_by('-date')[posts_per_page*(post_set-1):posts_per_page*post_set]
    elif 'older' in request.POST:
        post_set = int(request.POST.get("current_set")) + 1
        post_list = Post.objects.filter(
            date__lte=timezone.now(),
            post_active=True
        ).order_by('-date')[posts_per_page*(post_set-1):posts_per_page*post_set]
        print(post_set)
    else:
        post_list = Post.objects.filter(
            date__lte=timezone.now(),
            post_active = True
        ).order_by('-date')[:posts_per_page]
        post_set = 1

    context = {'user_list': user_list, 'post_list':post_list, 'post_set':post_set, 'max_sets':max_sets}
    return render(request, template_name, context)

def search(request):
    user_list = User.objects.all()
    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, './social_match/search.html', {'filter': user_filter})

def profile(request, user_id=None):
    user = request.user
    viewing_user = user
    if not user_id: # accessing user's own profile
        user = request.user
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('social_match:home'))

        if 'change_status' in request.POST:
            current_user = request.user
            current_user.status_active = not current_user.status_active
            current_user.save()
    else:
        try:
            viewing_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return render(request, './social_match/404.html')

    template_name = './social_match/profile.html'
    form = ProfileForm(initial={
        'first_name': viewing_user.first_name,
        'last_name': viewing_user.last_name,
        'phone': viewing_user.phone,
        'class_standing': viewing_user.class_standing,
        'graduation_year': viewing_user.graduation_year,
        'majors': viewing_user.majors,
        'minors': viewing_user.minors,
        'courses': viewing_user.courses,
        'interests': viewing_user.interests,
        'skills': viewing_user.skills,
        'activities': viewing_user.activities,
    })

    return render(request, template_name, {'user': user, 'viewing_user': viewing_user, 'form': ProfileForm})

def myposts(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('social_match:home'))

    posts_per_page = 20
    post_list = Post.objects.filter(
        user = request.user
    ).order_by('-date')

    max_sets = math.ceil(len(Post.objects.filter(
        user = request.user
    )) / posts_per_page)

    if 'newer' in request.POST:
        post_set = int(request.POST.get("current_set")) - 1
        post_list = Post.objects.filter(
            user=request.user
        ).order_by('-date')[posts_per_page*(post_set-1):posts_per_page*post_set]
    elif 'older' in request.POST:
        post_set = int(request.POST.get("current_set")) + 1
        post_list = Post.objects.filter(
            user=request.user
        ).order_by('-date')[posts_per_page*(post_set-1):posts_per_page*post_set]
        print(post_set)
    else:
        post_list = Post.objects.filter(
            user=request.user
        ).order_by('-date')[:posts_per_page]
        post_set = 1

    template_name = './social_match/myposts.html'
    context = {'post_list':post_list, 'post_set':post_set, 'max_sets':max_sets}
    return render(request, template_name, context)


def createpost(request):
    template_name = './social_match/createpost.html'

    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.date = datetime.now()
            post.save()

            message = 'Your post has been created!'
            form = PostForm()
            context = {'form':form, 'confirmation':message}
            return render(request, template_name, context)

    else:
        form = PostForm()

    return render(request, template_name, {'form': form})

def editpost(request, post_id):
    template_name = './social_match/editpost.html'
    post = Post.objects.get(id=post_id)

    if request.method == "POST":
        form = EditPostForm(request.POST)
        if form.has_changed() and form.is_valid():
            post.refresh_from_db()
            post.headline = form.cleaned_data.get('headline')
            post.message = form.cleaned_data.get('message')
            post.post_active = not form.cleaned_data.get('post_active')
            post.post_edited = True
            post.date_edited = datetime.now()
            post.save()

            return HttpResponseRedirect('/myposts')
    else:
        form = EditPostForm(initial={'headline':post.headline, 'message':post.message, 'post_active':(not post.post_active)})

    return render(request, template_name, {'form': form})