from django.contrib import admin

from .models import Recipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "created_at")
    list_filter = ("category", "created_at")
    search_fields = ("title", "description", "author__email")
    readonly_fields = ("created_at",)
