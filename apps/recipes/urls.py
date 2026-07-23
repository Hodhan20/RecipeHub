from django.urls import path

from . import views

app_name = "recipes"

urlpatterns = [
    path("", views.recipe_list, name="recipe_list"),
    path("create/", views.create_recipe, name="create_recipe"),
    path("<int:pk>/", views.recipe_detail, name="recipe_detail"),
    path("<int:pk>/edit/", views.edit_recipe, name="edit_recipe"),
    path("<int:pk>/delete/", views.delete_recipe, name="delete_recipe"),
    path("<int:pk>/favourite/", views.favourite_recipe, name="favourite_recipe"),
    path("favourites/", views.favourite_list, name="favourite_list"),
]
