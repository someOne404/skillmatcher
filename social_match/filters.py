from django.contrib.auth.models import User
from .models import User
import django_filters

class UserFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'class_standing', 'graduation_year',
                  'majors', 'minors', 'courses', 'skills', 'interests', 'activities']

    @property
    def qs(self):
        parent = super(UserFilter, self).qs
        return parent.filter(status_active=True, is_superuser=False)