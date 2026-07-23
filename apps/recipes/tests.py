from django.test import TestCase
from django.urls import reverse

from apps.recipes.models import Recipe
from apps.users.models import CustomUser


class RecipeListViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test@example.com",
            password="testpass123",
        )

    def test_recipe_list_status_code(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertEqual(response.status_code, 200)

    def test_recipe_list_template(self):
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertTemplateUsed(response, "recipes/recipe_list.html")

    def test_recipe_list_context(self):
        Recipe.objects.create(
            title="Test Recipe",
            category="lunch",
            description="A test recipe",
            ingredients="Flour, water",
            instructions="Mix and bake",
            author=self.user,
        )
        response = self.client.get(reverse("recipes:recipe_list"))
        self.assertEqual(len(response.context["recipes"]), 1)

    def test_recipe_list_search(self):
        Recipe.objects.create(
            title="Pancakes",
            category="breakfast",
            description="Fluffy pancakes",
            ingredients="Flour, eggs",
            instructions="Mix and fry",
            author=self.user,
        )
        Recipe.objects.create(
            title="Salad",
            category="lunch",
            description="Fresh salad",
            ingredients="Lettuce, tomato",
            instructions="Chop and mix",
            author=self.user,
        )
        response = self.client.get(reverse("recipes:recipe_list"), {"q": "Pancakes"})
        self.assertEqual(len(response.context["recipes"]), 1)
        self.assertEqual(response.context["recipes"][0].title, "Pancakes")

    def test_recipe_list_category_filter(self):
        Recipe.objects.create(
            title="Pancakes",
            category="breakfast",
            description="Fluffy pancakes",
            ingredients="Flour, eggs",
            instructions="Mix and fry",
            author=self.user,
        )
        response = self.client.get(reverse("recipes:recipe_list"), {"category": "breakfast"})
        self.assertEqual(len(response.context["recipes"]), 1)


class RecipeDetailViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test@example.com",
            password="testpass123",
        )
        self.recipe = Recipe.objects.create(
            title="Test Recipe",
            category="lunch",
            description="A test recipe",
            ingredients="Flour, water",
            instructions="Mix and bake",
            author=self.user,
        )

    def test_recipe_detail_status_code(self):
        response = self.client.get(reverse("recipes:recipe_detail", args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 200)

    def test_recipe_detail_template(self):
        response = self.client.get(reverse("recipes:recipe_detail", args=[self.recipe.pk]))
        self.assertTemplateUsed(response, "recipes/recipe_detail.html")

    def test_recipe_detail_content(self):
        response = self.client.get(reverse("recipes:recipe_detail", args=[self.recipe.pk]))
        self.assertContains(response, "Test Recipe")


class RecipeCreateViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test@example.com",
            password="testpass123",
        )

    def test_create_recipe_requires_login(self):
        response = self.client.get(reverse("recipes:create_recipe"))
        self.assertEqual(response.status_code, 302)

    def test_create_recipe_post(self):
        self.client.login(username="test@example.com", password="testpass123")
        response = self.client.post(
            reverse("recipes:create_recipe"),
            {
                "title": "New Recipe",
                "category": "lunch",
                "description": "Description here",
                "ingredients": "Ingredients here",
                "instructions": "Instructions here",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(title="New Recipe").exists())


class RecipeEditViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test@example.com",
            password="testpass123",
        )
        self.recipe = Recipe.objects.create(
            title="Original Title",
            category="lunch",
            description="Original description",
            ingredients="Original ingredients",
            instructions="Original instructions",
            author=self.user,
        )

    def test_edit_recipe_owner(self):
        self.client.login(username="test@example.com", password="testpass123")
        response = self.client.post(
            reverse("recipes:edit_recipe", args=[self.recipe.pk]),
            {
                "title": "Updated Title",
                "category": "dinner",
                "description": "Updated description",
                "ingredients": "Updated ingredients",
                "instructions": "Updated instructions",
            },
        )
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, "Updated Title")

    def test_edit_recipe_non_owner_redirect(self):
        other_user = CustomUser.objects.create_user(
            username="other@example.com",
            password="otherpass123",
        )
        self.client.login(username="other@example.com", password="otherpass123")
        response = self.client.post(
            reverse("recipes:edit_recipe", args=[self.recipe.pk]),
            {
                "title": "Hacked Title",
                "category": "dinner",
                "description": "Hacked",
                "ingredients": "Hacked",
                "instructions": "Hacked",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.recipe.refresh_from_db()
        self.assertEqual(self.recipe.title, "Original Title")


class RecipeDeleteViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test@example.com",
            password="testpass123",
        )
        self.recipe = Recipe.objects.create(
            title="To Delete",
            category="lunch",
            description="Delete me",
            ingredients="Flour",
            instructions="Bake",
            author=self.user,
        )

    def test_delete_recipe_owner(self):
        self.client.login(username="test@example.com", password="testpass123")
        response = self.client.post(reverse("recipes:delete_recipe", args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Recipe.objects.filter(pk=self.recipe.pk).exists())

    def test_delete_recipe_non_owner_redirect(self):
        other_user = CustomUser.objects.create_user(
            username="other@example.com",
            password="otherpass123",
        )
        self.client.login(username="other@example.com", password="otherpass123")
        response = self.client.post(reverse("recipes:delete_recipe", args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Recipe.objects.filter(pk=self.recipe.pk).exists())


class FavouriteViewTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            username="test@example.com",
            password="testpass123",
        )
        self.recipe = Recipe.objects.create(
            title="Fav Recipe",
            category="lunch",
            description="A favourite recipe",
            ingredients="Flour",
            instructions="Bake",
            author=self.user,
        )

    def test_favourite_recipe(self):
        self.client.login(username="test@example.com", password="testpass123")
        response = self.client.get(reverse("recipes:favourite_recipe", args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.recipe.favourites.filter(pk=self.user.pk).exists())

    def test_unfavourite_recipe(self):
        self.recipe.favourites.add(self.user)
        self.client.login(username="test@example.com", password="testpass123")
        response = self.client.get(reverse("recipes:favourite_recipe", args=[self.recipe.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.recipe.favourites.filter(pk=self.user.pk).exists())

    def test_favourite_list_requires_login(self):
        response = self.client.get(reverse("recipes:favourite_list"))
        self.assertEqual(response.status_code, 302)

    def test_favourite_list_template(self):
        self.recipe.favourites.add(self.user)
        self.client.login(username="test@example.com", password="testpass123")
        response = self.client.get(reverse("recipes:favourite_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "recipes/favourite_list.html")
