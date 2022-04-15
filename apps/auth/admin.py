from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin


@admin.register(get_user_model())
class UserAdmin(BaseUserAdmin):
    pass
