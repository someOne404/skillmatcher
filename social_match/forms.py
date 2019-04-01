from django import forms
from .models import *
from dal import autocomplete


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


class EditProfileForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ('first_name', 'last_name', 'phone',
				  'class_standing', 'graduation_year',
				  'majors', 'minors', 'skills',
				  'interests', 'courses', 'activities')
		widgets = {
			'courses': autocomplete.ModelSelect2Multiple(
				url='social_match:course-autocomplete',
			),
			'skills': autocomplete.ModelSelect2Multiple(
				url='social_match:skill-autocomplete',
			),
			'activities': autocomplete.ModelSelect2Multiple(
				url='social_match:activity-autocomplete',
			),
			'interests': autocomplete.ModelSelect2Multiple(
				url='social_match:interest-autocomplete',
			)
		}


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
