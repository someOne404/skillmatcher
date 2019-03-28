from django import forms
from .models import *

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('headline', 'message')

class EditPostForm(forms.ModelForm):
    post_active = forms.BooleanField(required=False)
    class Meta:
        model = Post
        fields = {'headline', 'message', 'post_active'}

class CommentPostForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={
                'id': 'comment-text',
                'required': True,
            })
        }

class PostSearchForm(forms.Form):
    name = forms.CharField(max_length=50, required=False)
    keywords = forms.CharField(max_length=200, required=False)
    liked = forms.BooleanField(required=False)
    commented = forms.BooleanField(required=False)

class EditProfileForm(forms.ModelForm):
    status_active = forms.BooleanField(required=False)
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 
        'class_standing', 'graduation_year',
        'majors', 'minors', 'skills',
        'interests','courses','activities','status_active')

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