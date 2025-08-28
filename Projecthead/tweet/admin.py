from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Tweet, CustomUser

# Register Tweet model
admin.site.register(Tweet)

# Custom UserAdmin for CustomUser
class CustomUserAdmin(UserAdmin):
    # Specify the fields to display in the admin list view
    list_display = (
        'username', 'email', 'first_name', 'last_name', 'is_staff', 'user_profile_image', 'user_bio'
    )

    # Fieldsets for the detail view of a user
    fieldsets = (
        (None, {
            'fields': ('username', 'password')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'user_profile_image', 'user_bio')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
        ('Important dates', {
            'fields': ('last_login', 'date_joined')
        }),
    )

    # Fieldsets for adding a new user
    add_fieldsets = (
        (None, {
            'fields': ('username', 'password1', 'password2')
        }),
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email', 'user_profile_image', 'user_bio')
        }),
        ('Permissions', {
            'fields': (
                'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'
            )
        }),
    )

# Register CustomUser with the custom admin
admin.site.register(CustomUser, CustomUserAdmin)
