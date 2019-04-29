from django.contrib.auth.models import User
from .models import *
import django_filters
from dal import autocomplete


class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    majors = django_filters.ModelMultipleChoiceFilter(queryset=Major.objects.all(),
                                                      conjoined=True,
                                                      widget=autocomplete.ModelSelect2Multiple(
                                                          url='social_match:major-autocomplete',
                                                          attrs={
                                                              'style': 'width:100% !important',
                                                              'data-theme': 'bootstrap'
                                                          },
                                                      )
          )
    minors = django_filters.ModelMultipleChoiceFilter(queryset=Minor.objects.all(),
                                                      conjoined=True,
                                                      widget=autocomplete.ModelSelect2Multiple(
                                                          url='social_match:minor-autocomplete',
                                                          attrs={
                                                              'style': 'width:100% !important',
                                                              'data-theme': 'bootstrap'
                                                          },
                                                      )
          )
    courses = django_filters.ModelMultipleChoiceFilter(queryset=Course.objects.all(),
                                                       conjoined=True,
                                                       widget=autocomplete.ModelSelect2Multiple(
                                                           url='social_match:course-autocomplete',
                                                          attrs={
                                                              'style': 'width:100% !important',
                                                              'data-theme': 'bootstrap'
                                                          },
                                                       )
           )
    skills = django_filters.ModelMultipleChoiceFilter(queryset=Skill.objects.all(),
                                                      conjoined=True,
                                                      widget=autocomplete.ModelSelect2Multiple(
                                                          url='social_match:skill-search',
                                                          attrs={
                                                              'style': 'width:100% !important',
                                                              'data-theme': 'bootstrap'
                                                          },
                                                      )
          )
    activities = django_filters.ModelMultipleChoiceFilter(queryset=Activity.objects.all(),
                                                          conjoined=True,
                                                          widget=autocomplete.ModelSelect2Multiple(
                                                              url='social_match:activity-search',
                                                              attrs={
                                                                  'style': 'width:100% !important',
                                                                  'data-theme': 'bootstrap'
                                                              },
                                                          )
              )
    interests = django_filters.ModelMultipleChoiceFilter(queryset=Interest.objects.all(),
                                                         conjoined=True,
                                                         widget=autocomplete.ModelSelect2Multiple(
                                                             url='social_match:interest-search',
                                                              attrs={
                                                                  'style': 'width:100% !important',
                                                                  'data-theme': 'bootstrap'
                                                              },
                                                         )
             )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'class_standing', 'graduation_year',
                  'majors', 'minors', 'courses', 'skills', 'interests', 'activities']

    @property
    def qs(self):
        parent = super(UserFilter, self).qs
        return parent.filter(status_active=True, is_superuser=False)