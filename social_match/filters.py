from django.contrib.auth.models import User
from .models import User
import django_filters

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'class_standing', 'graduation_year',]