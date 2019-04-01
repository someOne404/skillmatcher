from django.urls import path
from django.conf.urls import url
from . import views
from django_filters.views import FilterView
from social_match.filters import UserFilter
from .models import *

app_name = 'social_match'
urlpatterns = [
	path('', views.base, name='base'),
	path('about/', views.about, name='about'),
	path('home/', views.home, name='home'),
	url(r'^search/$', FilterView.as_view(filterset_class=UserFilter,
										 template_name='social_match/search.html'), name='search'),
	path('createpost/', views.createpost, name='createpost'),
	path('profile/', views.profile, name='profile'),
	path('profile/<int:user_id>/', views.profile, name='profile'),
	path('editprofile/<int:user_id>/', views.editprofile, name="editprofile"),
	path('myposts/', views.myposts, name='myposts'),
	path('likepost/', views.likepost, name="likepost"),
	path('commentpost/', views.commentpost, name="commentpost"),
	path('editpost/<int:post_id>/', views.editpost, name="editpost"),
	path('api/classes/', views.classlist, name='classlist'),
	path('api/majors/', views.majorlist, name='majorlist'),
	path('api/minors/', views.minorlist, name='minorlist'),
	path("api/course-autocomplete/", views.CourseAutocomplete.as_view(), name='course-autocomplete'),
	path("api/skill-autocomplete/", views.SkillAutocomplete.as_view(model=Skill, create_field='name'), name='skill-autocomplete'),
	path("api/activity-autocomplete/", views.ActivityAutocomplete.as_view(model=Activity, create_field='name'),
		 name='activity-autocomplete'),
	path("api/interest-autocomplete/", views.InterestAutocomplete.as_view(model=Interest, create_field='name'),
		 name='interest-autocomplete'),
]
