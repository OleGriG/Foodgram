from django.contrib import admin
from django.core.exceptions import ValidationError

from .models import (Favourite, Ingredient, IngredientInRecipe, Recipe,
                     ShoppingCart, Tag)


class IngredientInRecipeInline(admin.TabularInline):
    model = IngredientInRecipe


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'author', 'added_in_favorites',
                    'display_ingredients', 'tags', )
    readonly_fields = ('added_in_favorites',)
    list_filter = ('author', 'name', 'tags',)
    inlines = [IngredientInRecipeInline]
    search_fields = ('name', 'tags__name', 'author__username')

    @admin.display(description='Количество в избранных')
    def added_in_favorites(self, obj):
        return obj.favorites.count()

    @admin.display(description='Ингредиенты')
    def display_ingredients(self, obj):
        recipe_ingredient = obj.ingredients.all()
        return ", ".join([ingredient.name for ingredient in recipe_ingredient])


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_filter = ('name',)
    search_fields = ['name']

    def save_model(self, request, obj, form, change):
        if Ingredient.objects.filter(name=obj.name).exists():
            raise ValidationError("Ингредиент уже существует")

        super().save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color', 'slug',)


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe', 'recipe__ingredients', )


@admin.register(Favourite)
class FavouriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'recipe',)


@admin.register(IngredientInRecipe)
class IngredientInRecipe(admin.ModelAdmin):
    list_display = ('recipe', 'ingredient', 'amount',)
