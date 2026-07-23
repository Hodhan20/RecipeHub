from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            "title",
            "category",
            "description",
            "ingredients",
            "instructions",
            "image",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input input-bordered w-full"}),
            "category": forms.Select(attrs={"class": "select select-bordered w-full"}),
            "description": forms.Textarea(
                attrs={"class": "textarea textarea-bordered w-full", "rows": 4}
            ),
            "ingredients": forms.Textarea(
                attrs={"class": "textarea textarea-bordered w-full", "rows": 6}
            ),
            "instructions": forms.Textarea(
                attrs={"class": "textarea textarea-bordered w-full", "rows": 8}
            ),
            "image": forms.ClearableFileInput(attrs={"class": "file-input file-input-bordered w-full"}),
        }
