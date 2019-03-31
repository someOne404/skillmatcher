
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.template.loader import render_to_string
from django.core import serializers
import json
from django.db.models import Q
from django.core.paginator import Paginator

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
    template_name = './social_match/home.html'
    form = PostSearchForm()

    filtered = bool(request.GET.get('f'))
    keywordstr = request.GET.get('k')
    namestr = request.GET.get('n')
    liked = bool(request.GET.get('l'))
    commented = bool(request.GET.get('c'))

    if keywordstr is None:
        keywordstr = ""
    if namestr is None:
        namestr = ""

    # get current set of posts to display on page
    if_all = Q(date__lte=timezone.now(),post_active=True)
    if_any = Q()
    if request.method == 'POST':
        if 'filter' in request.POST:
            form = PostSearchForm(request.POST)
            if form.is_valid():
                keywordstr = form.cleaned_data['keywords']
                namestr = form.cleaned_data['name']
                liked = form.cleaned_data['liked']
                commented = form.cleaned_data['commented']
                filtered = True
        if 'clear' in request.POST:
            filtered = False
            keywordstr = ""
            namestr = ""
            liked = False
            commented = False

    keywords = keywordstr.split()
    names = namestr.split()
    for keyword in keywords:
        if_any |= Q(headline__icontains=keyword)
        if_any |= Q(message__icontains=keyword)
    for name in names:
        if_any |= Q(user__first_name__icontains=name)
        if_any |= Q(user__last_name__icontains=name)
    if liked:
        if_any |= Q(likes__id=request.user.id)
    if commented:
        if_any |= Q(comments__user__id=request.user.id)
    if_all &= if_any

    #ISSUE: likes and comments don't work after filtering
    #ISSUE: do same for myprofile posts
    #ISSUE: comments get really long - possibly compress them?

    posts_per_page= 20
    posts = Post.objects.filter(if_all).distinct().order_by('-date')
    paginator = Paginator(posts,posts_per_page)
    page = request.GET.get('p')
    post_list = paginator.get_page(page)

    context = {
        'post_list': post_list,
        'form': form,
        'keywords': keywordstr,
        'names': namestr,
        'liked': liked,
        'commented': commented,
        'filtered' :filtered,
    }
    return render(request, template_name, context)

def search(request):
    user_list = User.objects.all()
    print(user_list)
    # user_list.remove(request.user)

    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, './social_match/search.html', {'filter': user_filter})

def profile(request, user_id=None):
    user = request.user
    viewing_user = user
    if not user_id: # accessing user's own profile
        user = request.user
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('social_match:home'))

    else:
        try:
            viewing_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return render(request, './social_match/404.html')

    # get current set of posts to display on page
    posts_per_page = 5
    unordered_posts = Post.objects.filter(user=viewing_user)
    max_sets = math.ceil(len(unordered_posts) / posts_per_page)

    if 'newer' in request.POST:
        post_set = int(request.POST.get("current_set")) - 1
    elif 'older' in request.POST:
        post_set = int(request.POST.get("current_set")) + 1
    else:
        post_set = 1
    post_list = unordered_posts.order_by('-date')[posts_per_page * (post_set - 1):posts_per_page * post_set]

    template_name = './social_match/profile.html'

    return render(request, template_name, {
        'user': user,
        'viewing_user': viewing_user,
        'post_list':post_list,
        'post_set':post_set,
        'max_sets':max_sets,
    })

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

            return HttpResponseRedirect('/profile')
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

    template_name = './social_match/home_posts.html'

    filtered = not bool(request.POST.get('f'))
    keywordstr = request.POST.get('k')
    namestr = request.POST.get('n')
    liked = not bool(request.POST.get('l'))
    commented = not bool(request.POST.get('c'))
    if keywordstr is None:
        keywordstr = ""
    if namestr is None:
        namestr = ""
    if_all = Q(date__lte=timezone.now(), post_active=True)
    if_any = Q()
    keywords = keywordstr.split()
    names = namestr.split()
    for keyword in keywords:
        if_any |= Q(headline__icontains=keyword)
        if_any |= Q(message__icontains=keyword)
    for name in names:
        if_any |= Q(user__first_name__icontains=name)
        if_any |= Q(user__last_name__icontains=name)
    if liked:
        if_any |= Q(likes__id=request.user.id)
    if commented:
        if_any |= Q(comments__user__id=request.user.id)
    if_all &= if_any

    posts_per_page = 20
    posts = Post.objects.filter(if_all).distinct().order_by('-date')
    paginator = Paginator(posts,posts_per_page)
    page = request.POST.get('p')
    post_list = paginator.get_page(page)

    context = {
        'post_list': post_list,
        'form': PostSearchForm(),
        'keywords': keywordstr,
        'names': namestr,
        'liked': liked,
        'commented': commented,
        'filtered': filtered,
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

    template_name = './social_match/home_posts.html'

    filtered = not bool(request.POST.get('f'))
    keywordstr = request.POST.get('k')
    namestr = request.POST.get('n')
    liked = not bool(request.POST.get('l'))
    commented = not bool(request.POST.get('c'))
    if keywordstr is None:
        keywordstr = ""
    if namestr is None:
        namestr = ""

    if_all = Q(date__lte=timezone.now(), post_active=True)
    if_any = Q()
    keywords = keywordstr.split()
    names = namestr.split()
    for keyword in keywords:
        if_any |= Q(headline__icontains=keyword)
        if_any |= Q(message__icontains=keyword)
    for name in names:
        if_any |= Q(user__first_name__icontains=name)
        if_any |= Q(user__last_name__icontains=name)
    if liked:
        if_any |= Q(likes__id=request.user.id)
    if commented:
        if_any |= Q(comments__user__id=request.user.id)
    if_all &= if_any

    posts_per_page = 20
    posts = Post.objects.filter(if_all).distinct().order_by('-date')
    paginator = Paginator(posts, posts_per_page)
    page = request.POST.get('p')
    post_list = paginator.get_page(page)

    context = {
        'post_list': post_list,
        'form': PostSearchForm(),
        'keywords': keywordstr,
        'names': namestr,
        'liked': liked,
        'commented': commented,
        'filtered': filtered,
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
            user.status_active = form.cleaned_data.get('status_active')
            user.save()

            return HttpResponseRedirect('/profile')
    else:
        form = EditProfileForm(instance = user)

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
