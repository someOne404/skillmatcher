from django.contrib import admin
from django.contrib.auth import forms as auth_forms
from django import forms
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from social_match.models import User


class UserAdmin(BaseUserAdmin):
	form = auth_forms.UserChangeForm
	add_form = auth_forms.UserCreationForm

	list_display = ('id', 'email', 'username', 'first_name', 'last_name', )
	fieldsets = (
		(None, {'fields': ('email', 'password',)}),
		('Personal info', {'fields': ('first_name', 'last_name', 'username', 'date_joined', 'last_login', )}),
		('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions',)}),
		('User', {'fields': ()}),
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