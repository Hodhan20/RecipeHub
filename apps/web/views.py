from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _

from apps.recipes.models import Recipe
from apps.users.models import CustomUser


def home(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect("web:admin_dashboard")
        return redirect("web:user_dashboard")
    return render(request, "web/landing_page.html")


@login_required
def user_dashboard(request):
    recent_recipes = Recipe.objects.filter(author=request.user).order_by("-created_at")[:6]
    total_recipes = Recipe.objects.filter(author=request.user).count()
    total_favourites = request.user.favourite_recipes.count()
    return render(
        request,
        "web/app_home.html",
        {
            "active_tab": "dashboard",
            "page_title": _("My Dashboard"),
            "recent_recipes": recent_recipes,
            "total_recipes": total_recipes,
            "total_favourites": total_favourites,
        },
    )


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    total_users = CustomUser.objects.count()
    total_recipes = Recipe.objects.count()
    total_favourites = Recipe.favourites.through.objects.count()
    recent_recipes = Recipe.objects.all().order_by("-created_at")[:6]
    recent_users = CustomUser.objects.all().order_by("-date_joined")[:6]
    return render(
        request,
        "web/admin_dashboard.html",
        {
            "active_tab": "admin_dashboard",
            "page_title": _("Admin Dashboard"),
            "total_users": total_users,
            "total_recipes": total_recipes,
            "total_favourites": total_favourites,
            "recent_recipes": recent_recipes,
            "recent_users": recent_users,
        },
    )


@user_passes_test(lambda u: u.is_superuser)
def simulate_error(request):
    raise Exception("This is a simulated error.")
