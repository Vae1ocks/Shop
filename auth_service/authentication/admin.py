from django.contrib import admin

from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "first_name", "is_verified"]
    list_filter = ["is_verified"]
    list_per_page = 30
    search_fields = ["email", "first_name"]
