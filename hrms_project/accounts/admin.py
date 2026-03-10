from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ['-date_joined']
    list_display = [
        'email',
        'first_name',
        'last_name',
        'role',
        'is_active',
        'is_staff',
        'date_joined',
    ]
    list_filter = ['role', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['date_joined', 'last_login']

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'phone', 'profile_picture', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important Dates', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'role',
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )
