from allauth.account.models import EmailAddress
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.recipes.models import Recipe
from .forms import CustomUserChangeForm, UploadAvatarForm
from .helpers import require_email_confirmation, user_has_confirmed_email_address
from .models import CustomUser


@login_required
def profile(request):
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user_before_update = CustomUser.objects.get(pk=user.pk)
            email_changed = user_before_update.email != user.email
            need_to_confirm_email = (
                email_changed
                and require_email_confirmation()
                and not user_has_confirmed_email_address(user, user.email)
            )
            if need_to_confirm_email:
                new_email = user.email
                EmailAddress.objects.add_email(request, user, new_email, confirm=True)
                user.email = user_before_update.email
                form = CustomUserChangeForm(instance=user)
            user.save()

            if email_changed and not need_to_confirm_email:
                email_address = EmailAddress.objects.filter(user=user, email__iexact=user.email).first()
                if email_address:
                    email_address.set_as_primary()
            messages.success(request, _("Profile successfully saved."))
    else:
        form = CustomUserChangeForm(instance=request.user)

    user_recipes = Recipe.objects.filter(author=request.user).order_by("-created_at")[:6]

    return render(
        request,
        "account/profile.html",
        {
            "form": form,
            "active_tab": "profile",
            "page_title": _("Profile"),
            "user_recipes": user_recipes,
        },
    )


@login_required
@require_POST
def upload_profile_image(request):
    user = request.user
    form = UploadAvatarForm(request.POST, request.FILES)
    if form.is_valid():
        user.avatar = request.FILES["avatar"]
        user.save()
        return JsonResponse({"avatar_url": user.avatar_url})
    else:
        readable_errors = ", ".join(str(error) for key, errors in form.errors.items() for error in errors)
        return JsonResponse(status=400, data={"errors": readable_errors})


@login_required
def my_recipes(request):
    recipes = Recipe.objects.filter(author=request.user).order_by("-created_at")
    return render(
        request,
        "recipes/my_recipes.html",
        {
            "recipes": recipes,
            "page_title": _("My Recipes"),
        },
    )
