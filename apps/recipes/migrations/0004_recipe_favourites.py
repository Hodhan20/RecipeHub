from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0003_alter_recipe_category"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="updated_at",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="recipe",
            name="favourites",
            field=models.ManyToManyField(
                blank=True,
                related_name="favourite_recipes",
                to="users.customuser",
            ),
        ),
    ]
