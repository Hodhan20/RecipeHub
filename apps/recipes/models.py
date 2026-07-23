from django.conf import settings
from django.db import models

from apps.utils.models import BaseModel


class Recipe(BaseModel):

    CATEGORY_CHOICES = [
        ("breakfast", "Breakfast"),
        ("lunch", "Lunch"),
        ("dinner", "Dinner"),
        ("dessert", "Dessert"),
        ("snacks", "Snacks"),
    ]

    title = models.CharField(max_length=200)
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default="breakfast",
    )
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="recipes",
    )

    favourites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name="favourite_recipes",
        blank=True,
    )

    def __str__(self):
        return self.title