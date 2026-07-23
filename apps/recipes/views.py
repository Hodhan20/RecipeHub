from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RecipeForm
from .models import Recipe


def recipe_list(request):
    query = request.GET.get("q")
    category = request.GET.get("category")

    recipes = Recipe.objects.all().select_related("author").order_by("-created_at")

    if query:
        recipes = recipes.filter(title__icontains=query)

    if category:
        recipes = recipes.filter(category=category)

    return render(
        request,
        "recipes/recipe_list.html",
        {
            "recipes": recipes,
            "query": query,
            "selected_category": category,
            "categories": Recipe.CATEGORY_CHOICES,
        },
    )


@login_required
def create_recipe(request):
    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES)

        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.author = request.user
            recipe.save()
            return redirect("recipes:recipe_detail", pk=recipe.pk)
    else:
        form = RecipeForm()

    return render(
        request,
        "recipes/recipe_form.html",
        {
            "form": form,
            "title": "Share a Recipe",
        },
    )


def recipe_detail(request, pk):
    recipe = get_object_or_404(Recipe.objects.select_related("author"), pk=pk)
    is_favourite = False
    if request.user.is_authenticated:
        is_favourite = recipe.favourites.filter(pk=request.user.pk).exists()

    return render(
        request,
        "recipes/recipe_detail.html",
        {
            "recipe": recipe,
            "is_favourite": is_favourite,
        },
    )


@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author != request.user:
        return redirect("recipes:recipe_list")

    if request.method == "POST":
        form = RecipeForm(request.POST, request.FILES, instance=recipe)

        if form.is_valid():
            form.save()
            return redirect("recipes:recipe_detail", pk=recipe.pk)
    else:
        form = RecipeForm(instance=recipe)

    return render(
        request,
        "recipes/recipe_form.html",
        {
            "form": form,
            "title": "Edit Recipe",
            "recipe": recipe,
        },
    )


@login_required
def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if recipe.author != request.user:
        return redirect("recipes:recipe_list")

    if request.method == "POST":
        recipe.delete()
        return redirect("recipes:recipe_list")

    return render(
        request,
        "recipes/recipe_confirm_delete.html",
        {
            "recipe": recipe,
        },
    )


@login_required
def favourite_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    if recipe.favourites.filter(pk=request.user.pk).exists():
        recipe.favourites.remove(request.user)
    else:
        recipe.favourites.add(request.user)
    return redirect("recipes:recipe_detail", pk=pk)


@login_required
def favourite_list(request):
    favourites = request.user.favourite_recipes.all().select_related("author")
    return render(
        request,
        "recipes/favourite_list.html",
        {
            "recipes": favourites,
        },
    )
