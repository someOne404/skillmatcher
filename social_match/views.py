from dal import autocomplete
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from friendship.models import Follow, Block
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.urls import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.template.loader import render_to_string
from django.core import serializers
from django.db.models import CharField, Value as V
from django.db.models.functions import Cast, Concat
import json
from django.db.models import Q
from django.core.paginator import Paginator

from django.db.models.signals import post_save, m2m_changed
from notifications.signals import notify
from notifications.models import *

from .models import *
from .filters import UserFilter
from .forms import *

import math

User = get_user_model()


def base(request):
	return HttpResponseRedirect(reverse('social_match:home'))


def about(request):
	template_name = './social_match/about.html'
	return render(request, template_name)


def home(request):
    template_name = './social_match/home.html'
    form = PostSearchForm()

    keywordstr, namestr, liked, commented, filtered = get_filter_form_results(request)

    posts_per_page = 20
    post_list = get_home_post_list(keywordstr, namestr, liked, commented, request.GET.get('p'), request.user.id, posts_per_page)

    if request.user.is_authenticated:
        request_user = User.objects.get(id=request.user.id)
        notifications = Notification.objects.filter(recipient=request_user, unread=True)
    else:
        notifications = []

    #show unread notifications on home
    #show all notifications on profile

    context = {
        'post_list': post_list,
        'form': form,
        'keywords': keywordstr,
        'names': namestr,
        'liked': liked,
        'commented': commented,
        'filtered': filtered,
        'notifications': notifications,
    }
    return render(request, template_name, context)

def search(request):
    user_list = User.objects.all()
    #print(user_list)
    # user_list.remove(request.user)

    user_filter = UserFilter(request.GET, queryset=user_list)
    return render(request, './social_match/search.html', {'filter': user_filter})

def resetsearch(request):
    return render(request, './social_match/search.html')

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

    following_list = Follow.objects.following(user)
    if viewing_user in following_list:
        check_follow = True
    else:
        check_follow = False

    blocking_list = Block.objects.blocking(user)

    if viewing_user in blocking_list:
        check_block = True
    else:
        check_block = False



    posts_per_page = 5
    post_list = get_profile_post_list(viewing_user, posts_per_page, request.GET.get('p'))

    notifications = Notification.objects.filter(recipient=viewing_user)

    template_name = './social_match/profile.html'

    #uploading files
    if request.method == 'POST' and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, template_name, {
            'user': user,
            'viewing_user': viewing_user,
            'post_list':post_list,
            'uploaded_file_url': uploaded_file_url
        })
    
    return render(request, template_name, {
        'user': user,
        'viewing_user': viewing_user,
        'form': ProfileForm,
        'post_list':post_list,
        #'post_set':post_set,
        #'max_sets':max_sets,
        'check_follow': check_follow,
        'check_block': check_block,
        'post_list': post_list,
        'notifications': notifications,
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
			context = {'form': form, 'confirmation': message}
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

    template = request.POST.get('t')
    if template == "home":
        template_name = './social_match/home_posts.html'

        keywordstr, namestr, liked, commented, filtered = get_filter_inputs(request)

        posts_per_page = 20
        post_list = get_home_post_list(keywordstr, namestr, liked, commented, request.POST.get('p'), request.user.id, posts_per_page)

        context = {
            'post_list': post_list,
            'keywords': keywordstr,
            'names': namestr,
            'liked': liked,
            'commented': commented,
            'filtered': filtered,
        }

    else:
        template_name = './social_match/profile_posts.html'

        user_id = request.POST.get('u')
        if not user_id:  # accessing user's own profile
            user = request.user
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('social_match:home'))
        else:
            try:
                viewing_user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return render(request, './social_match/404.html')

        posts_per_page = 5
        post_list = get_profile_post_list(viewing_user, posts_per_page, request.POST.get('p'))

        context = {
            'user': request.user,
            'viewing_user': viewing_user,
            'post_list': post_list,
        }

    if request.is_ajax():
        html = render_to_string(template_name, context, request=request)
        return JsonResponse({'form': html})

def commentpost(request):
    id = request.POST.get('id')
    form = None
    if request.POST.get('type') == 'comment':
        form = CommentPostForm()
    if request.POST.get('type') == 'submitcomment':
        post = get_object_or_404(Post, id=id)
        if request.POST.get('text') != '':
            comment = Comment()
            comment.text = request.POST.get('text')
            comment.user = request.user
            comment.date = timezone.now()
            comment.post = post
            comment.save()
        form = None
    if request.POST.get('type') == 'deletecomment':
        comment = get_object_or_404(Comment, id=id)
        comment.delete()
        form = None

    template = request.POST.get('t')
    if template == "home":
        template_name = './social_match/home_posts.html'

        keywordstr, namestr, liked, commented, filtered = get_filter_inputs(request)

        posts_per_page = 20
        post_list = get_home_post_list(keywordstr, namestr, liked, commented, request.POST.get('p'), request.user.id, posts_per_page)

        context = {
            'post_list': post_list,
            'keywords': keywordstr,
            'names': namestr,
            'liked': liked,
            'commented': commented,
            'filtered': filtered,
            'post_id': int(id,10),
            'form': form
        }
    else:
        template_name = './social_match/profile_posts.html'

        user_id = request.POST.get('u')
        if not user_id:  # accessing user's own profile
            user = request.user
            if not request.user.is_authenticated:
                return HttpResponseRedirect(reverse('social_match:home'))
        else:
            try:
                viewing_user = User.objects.get(id=user_id)
            except User.DoesNotExist:
                return render(request, './social_match/404.html')

        posts_per_page = 5
        post_list = get_profile_post_list(viewing_user, posts_per_page, request.POST.get('p'))

        context = {
            'user': request.user,
            'viewing_user': viewing_user,
            'post_list': post_list,
            'post_id': int(id, 10),
            'form': form,
        }

    if request.is_ajax():
        html = render_to_string(template_name, context, request=request)
        return JsonResponse({'form': html})

def notifications(request, notification_id):
    notification = get_object_or_404(Notification, id=notification_id)
    if 'read' in request.GET:
        notification.mark_as_read()
    if 'delete' in request.GET:
        notification.delete()

    return_to = request.GET.get("return_to")
    if return_to == "home":
        return HttpResponseRedirect('/home')
    else:
        return HttpResponseRedirect('/profile')

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
			user.save()

			return HttpResponseRedirect('/profile')
	else:
		form = EditProfileForm(instance=user)
		print("check perms")
		# add permissions for creating options
		perm1 = Permission.objects.get(name="Can add skill")
		perm2 = Permission.objects.get(name="Can add activity")
		perm3 = Permission.objects.get(name="Can add interest")
		if isinstance(request.user, User):
			if not request.user.has_perm(perm1):
				print("Added permission 1")
				request.user.user_permissions.add(perm1)
			else:
				print("Has permission")
			if not request.user.has_perm(perm2):
				request.user.user_permissions.add(perm2)
			if not request.user.has_perm(perm3):
				request.user.user_permissions.add(perm3)

	return render(request, template_name, {'form': form})


def classlist(request):
	courses = Course.objects.all()
	data = [{"name": str(c) + ": " + c.name} for c in courses]
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')

def majorlist(request):
	majors = Major.objects.all()
	data = [{"name": str(m) + ": " + m.name} for m in majors]
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')


def minorlist(request):
	minors = Minor.objects.all()
	data = [{"name": str(m) + ": " + m.name} for m in minors]
	json_data = json.dumps(data)
	return HttpResponse(json_data, content_type='application/json')

def follow(request, user_id):
    self = request.user
    other = User.objects.get(id=user_id)
    if other not in Follow.objects.following(self):
        Follow.objects.add_follower(self, other)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'follow': True})

def unfollow(request, user_id):
    self = request.user
    other = User.objects.get(id=user_id)
    if other in Follow.objects.following(self):
        Follow.objects.remove_follower(self, other)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'unfollow': True})

def following(request):
    return render(request, './social_match/following.html')

def follower(request):
    return render(request, './social_match/follower.html')


def block(request, user_id):
    self = request.user
    other = User.objects.get(id=user_id)
    if other not in Block.objects.blocking(self):
        Block.objects.add_block(self, other)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'block': True})

def unblock(request, user_id):
    self = request.user
    other = User.objects.get(id=user_id)
    if other in Block.objects.blocking(self):
        Block.objects.remove_block(self, other)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'), {'unblock': True})

class MajorAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated:
			return Major.objects.none()

		# search by course name and/or number
		qs = Major.objects.all()

		if self.q:
			qs = qs.filter(name__icontains=self.q)

		return qs


class MinorAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated:
			return Minor.objects.none()

		# search by course name and/or number
		qs = Minor.objects.all()

		if self.q:
			qs = qs.filter(name__icontains=self.q)

		return qs


class CourseAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated:
			return Course.objects.none()

		# search by course name and/or number
		qs = Course.objects.annotate(
			full_name=Concat('department', V(' '), Cast('number', CharField()), V(': '), 'name'))

		if self.q:
			qs = qs.filter(full_name__icontains=self.q)

		return qs


class SkillAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated:
			return Skill.objects.none()

		# search by course name and/or number
		qs = Skill.objects.all()

		if self.q:
			qs = qs.filter(name__icontains=self.q)

		return qs


class ActivityAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated:
			return Activity.objects.none()

		# search by course name and/or number
		qs = Activity.objects.all()

		if self.q:
			qs = qs.filter(name__icontains=self.q)

		return qs


class InterestAutocomplete(autocomplete.Select2QuerySetView):
	def get_queryset(self):
		# Don't forget to filter out results depending on the visitor !
		if not self.request.user.is_authenticated:
			return Interest.objects.none()

		# search by course name and/or number
		qs = Interest.objects.all()

		if self.q:
			qs = qs.filter(name__icontains=self.q)

		return qs

def get_profile_post_list(viewing_user, posts_per_page, page):
    posts = Post.objects.filter(user=viewing_user).order_by('-date')
    paginator = Paginator(posts, posts_per_page)
    post_list = paginator.get_page(page)
    return post_list

def post_filter(keywordstr, namestr, liked, commented, user_id):
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
        if_any |= Q(likes__id=user_id)
    if commented:
        if_any |= Q(comments__user__id=user_id)
    if_all &= if_any

    posts = Post.objects.filter(if_all).distinct().order_by('-date')
    return posts

def get_home_post_list(keywordstr, namestr, liked, commented, page, user_id, posts_per_page):
    posts = post_filter(keywordstr, namestr, liked, commented, user_id)
    paginator = Paginator(posts, posts_per_page)
    post_list = paginator.get_page(page)

    return post_list

def get_filter_inputs(request):

    if request.method == 'GET':
        if request.GET.get('f') == "True":
            filtered = True
        else:
            filtered = False
        if request.GET.get('l') == "True":
            liked = True
        else:
            liked = False
        if request.GET.get('c') == "True":
            commented = True
        else:
            commented = False
        keywordstr = request.GET.get('k')
        namestr = request.GET.get('n')
        if keywordstr is None:
            keywordstr = ""
        if namestr is None:
            namestr = ""
    elif request.method == 'POST':
        if request.POST.get('f') == "True":
            filtered = True
        else:
            filtered = False
        if request.POST.get('l') == "True":
            liked = True
        else:
            liked = False
        if request.POST.get('c') == "True":
            commented = True
        else:
            commented = False
        keywordstr = request.POST.get('k')
        namestr = request.POST.get('n')
        if keywordstr is None:
            keywordstr = ""
        if namestr is None:
            namestr = ""
    else:
        filtered = False
        keywordstr = ""
        namestr = ""
        liked = False
        commented = False

    return keywordstr, namestr, liked, commented, filtered

def get_filter_form_results(request):
    keywordstr, namestr, liked, commented, filtered = get_filter_inputs(request)

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

    return keywordstr, namestr, liked, commented, filtered

# "save" signal handling for comments created on Posts
def commentHandler(sender, instance, created, **kwargs):
    user_sender = User.objects.get(id=instance.user.id)
    user_recipient = User.objects.get(id=instance.post.user.id)
    post = Post.objects.get(id=instance.post.id)

    if user_sender != user_recipient:
        # target: post commented on
        # action_object: comment created on post
        # sender: user commenting on post
        # recipient: user receiving notification
        # verb: action description
        notify.send(target=post, action_object=instance, sender=user_sender, recipient=user_recipient, verb='commented')

post_save.connect(commentHandler, sender=Comment)

# "save" signal handling for likes added to Posts
def likeHandler(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for i in pk_set: # always a single element in this set
            sender_id = i
        user_sender = User.objects.get(id=sender_id)
        user_recipient = User.objects.get(id=instance.user.id)

        if user_sender != user_recipient:
            # target: post liked
            # sender: user liking post
            # recipient: user receiving notification
            # verb: action description
            notify.send(target=instance, sender=user_sender, recipient=user_recipient, verb='liked')

m2m_changed.connect(likeHandler, sender=Post.likes.through)
