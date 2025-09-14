
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Book, CustomUser

admin.site.register(Book)

# Custom admin for CustomUser
class CustomUserAdmin(UserAdmin):
	model = CustomUser
	fieldsets = UserAdmin.fieldsets + (
		(None, {'fields': ('date_of_birth', 'profile_photo')}),
	)
	add_fieldsets = UserAdmin.add_fieldsets + (
		(None, {'fields': ('date_of_birth', 'profile_photo')}),
	)
	list_display = ['username', 'email', 'date_of_birth', 'is_staff']

admin.site.register(CustomUser, CustomUserAdmin)