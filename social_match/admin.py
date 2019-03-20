from django.contrib import admin
from django.contrib.auth import forms as auth_forms
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.admin import ModelAdmin


from social_match.models import *


class UserAdmin(BaseUserAdmin):
	form = auth_forms.UserChangeForm
	add_form = auth_forms.UserCreationForm

	list_display = ('id', 'email', 'username', 'first_name', 'last_name', )
	fieldsets = (
		(None, {'fields': ('email', 'password',)}),
		('Personal info', {'fields': ('first_name', 'last_name', 'phone', 'graduation_year', 'class_standing', 'picture',
										'majors', 'minors', 'skills', 'interests', 'courses', 'activities', 'username',
									  	'date_joined', 'last_login', 'status_active')}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
	)
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('email', 'password', 'first_name', 'last_name',)}
		 ),
	)
	search_fields = ('id', 'email', 'first_name', 'last_name',)

	class Meta:
		model = User


admin.site.register(User, UserAdmin)
admin.site.register(Major, ModelAdmin)
admin.site.register(Minor, ModelAdmin)
admin.site.register(Course, ModelAdmin)
admin.site.register(Skill, ModelAdmin)
admin.site.register(Activity, ModelAdmin)
admin.site.register(Interest, ModelAdmin)
admin.site.register(Post, ModelAdmin)
admin.site.register(Comment, ModelAdmin)