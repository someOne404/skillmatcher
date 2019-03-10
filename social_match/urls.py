from django.urls import path
from django.conf.urls import url
from . import views
from django_filters.views import FilterView
from social_match.filters import UserFilter

app_name = 'social_match'
urlpatterns = [
    path('', views.base, name='base'),
    path('about/', views.about, name='about'),
    path('home/', views.home, name='home'),
    url(r'^search/$', FilterView.as_view(filterset_class=UserFilter,
        template_name='social_match/search.html'), name='search'),
    path('createpost/', views.createpost, name='createpost'),
    path('profile/', views.profile, name='profile'),
    path('myposts/', views.myposts, name='myposts'),
    path('likepost/', views.likepost, name="likepost"),
    path('editpost/<int:post_id>/', views.editpost, name="editpost"),
]