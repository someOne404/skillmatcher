
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from django.urls import reverse
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.template.loader import render_to_string
from django.core import serializers
import json

from .models import *
from .filters import UserFilter
from .forms import *

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
    else:
        post_list = Post.objects.filter(
            date__lte=timezone.now(),
            post_active = True
        ).order_by('-date')[:posts_per_page]
        post_set = 1

    context = {
        'user_list': user_list,
        'post_list': post_list,
        'post_set': post_set,
        'max_sets': max_sets
    }
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
            post.date = timezone.now()
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
            post.date_edited = timezone.now()
            post.save()

            return HttpResponseRedirect('/myposts')
    else:
        form = EditPostForm(initial={
            'headline':post.headline,
            'message':post.message,
            'post_active':(not post.post_active)
        })

    return render(request, template_name, {'form': form})

def likepost(request):
    post = get_object_or_404(Post, id=request.POST.get('id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user.id)
    else:
        post.likes.add(request.user.id)

    posts_per_page = 20
    template_name = './social_match/home_posts.html'
    user_list = User.objects.filter(status_active=True, is_superuser=False)
    max_sets = math.ceil(len(Post.objects.filter(
        date__lte=timezone.now(),
        post_active=True
    )) / posts_per_page)
    post_set = int(request.POST.get("current_set"))
    post_list = Post.objects.filter(
        date__lte=timezone.now(),
        post_active=True
    ).order_by('-date')[posts_per_page * (post_set - 1):posts_per_page * post_set]

    context = {
        'user_list': user_list,
        'post_list': post_list,
        'post_set': post_set,
        'max_sets': max_sets
    }

    if request.is_ajax():
        html = render_to_string(template_name, context, request=request)
        return JsonResponse({'form': html})

def commentpost(request):
    post_id = request.POST.get('id')
    post = get_object_or_404(Post, id=post_id)
    form = None
    if request.POST.get('type') == 'comment':
        form = CommentPostForm()
    if request.POST.get('type') == 'submitcomment':
        if request.POST.get('text') != '':
            comment = Comment()
            comment.text = request.POST.get('text')
            comment.user = request.user
            comment.date = timezone.now()
            comment.post = post
            comment.save()
        form = None
        
    posts_per_page = 20
    template_name = './social_match/home_posts.html'
    user_list = User.objects.filter(status_active=True, is_superuser=False)
    max_sets = math.ceil(len(Post.objects.filter(
        date__lte=timezone.now(),
        post_active=True
    )) / posts_per_page)
    post_set = int(request.POST.get("current_set"))
    post_list = Post.objects.filter(
        date__lte=timezone.now(),
        post_active=True
    ).order_by('-date')[posts_per_page * (post_set - 1):posts_per_page * post_set]

    context = {
        'user_list': user_list,
        'post_list': post_list,
        'post_set': post_set,
        'max_sets': max_sets,
        'post_id': int(post_id,10),
        'form': form
    }

    if request.is_ajax():
        html = render_to_string(template_name, context, request=request)
        return JsonResponse({'form': html})

def editprofile(request, user_id):
    template_name = './social_match/editprofile.html'
    user = User.objects.get(id=user_id)
    if request.method == "POST":
        form = EditProfileForm(request.POST)

        if form.has_changed() and form.is_valid():
            user.refresh_from_db()

            return HttpResponse(user.phone)

            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.phone = form.cleaned_data.get('phone')
            user.class_standing = form.cleaned_data.get('class_standing')
            user.graduation_year = form.cleaned_data.get('graduation_year')

            user.majors.set(form.cleaned_data.get('majors'))
            user.minors.set(form.cleaned_data.get('minors'))
            user.skills.set(form.cleaned_data.get('skills'))
            user.interests.set(form.cleaned_data.get('interests'))
            user.courses.set(form.cleaned_data.get('courses'))
            user.activities.set(form.cleaned_data.get('activities'))
            user.save()

            return HttpResponseRedirect('/profile')
    else:
        form = EditProfileForm(initial={
            'first_name':user.first_name,
            'last_name':user.last_name,
            'phone':user.phone, 
            'class_standing':user.class_standing,
            'graduation_year':user.graduation_year,
            'majors':user.majors, 
            'minors':user.minors,
            'skills':user.skills,
            'interests':user.interests, 
            'courses':user.courses,
            'activities':user.activities,
        })

    return render(request, template_name, {'form': form})

def classlist(request):
    courses = Course.objects.all()
    data = [{"name": str(c)+": " + c.name} for c in courses]
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def majorlist(request):
    majors = Major.objects.all()
    data = [{"name": str(m)+": " + m.name} for m in majors]
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')


def minorlist(request):
    minors = Minor.objects.all()
    data = [{"name": str(m)+": " + m.name} for m in minors]
    json_data = json.dumps(data)
    return HttpResponse(json_data, content_type='application/json')
