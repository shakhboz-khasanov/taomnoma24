"""
Django admin configuration for core app
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    """
    Defines the admin pages for users
    """
    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {'fields': (
                'is_active',
                'is_staff',
                'is_superuser'
            )}
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    readonly_fields = ('last_login',)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }
        ),
    )


class RecipeAdmin(admin.ModelAdmin):
    """
    Defines the admin pages for recipes
    """
    ordering = ['id']
    list_display = ['title', 'user', 'time_minutes', 'price']
    list_filter = ['user', 'time_minutes', 'price']
    search_fields = ['title', 'description']


class TagAdmin(admin.ModelAdmin):
    """
    Defines the admin pages for tags
    """
    ordering = ['-id']
    list_display = ['name', 'user']
    search_fields = ['name']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Recipe, RecipeAdmin)
admin.site.register(models.Tag)
