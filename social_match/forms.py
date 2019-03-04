from django import forms
from .models import *

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('headline', 'message', 'user', 'date')

class ProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in self.initial:
                field.initial = self.initial[field_name]

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'graduation_year', 'class_standing', 'picture',
                    'majors', 'minors', 'skills', 'interests', 'courses', 'activities',)