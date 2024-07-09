from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'get_fullName']

    fieldsets = [
        (None, {
            'fields': ('username', 'email', 'first_name', 'last_name', 'phone'),
        }),
        ('Avatar', {
            'fields': ('avatar',),
        }),
    ]

    def get_fullName(self, obj):
        return f"{obj.first_name} {obj.last_name}"

    get_fullName.short_description = 'Full Name'