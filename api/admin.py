from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Recipe, Ingredient, Category, RecipeIngredient

# Your existing User admin registration
class CustomUserAdmin(BaseUserAdmin):
    pass

admin.site.register(User, CustomUserAdmin)


# Inline admin for RecipeIngredient, to edit ingredients per recipe with quantity and unit
class RecipeIngredientInline(admin.TabularInline):
    model = RecipeIngredient
    extra = 1
    autocomplete_fields = ['ingredient']  # Optional: searchable dropdown for ingredients

@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    inlines = [RecipeIngredientInline]
    list_display = ('title', 'user', 'prep_time', 'cooking_time', 'servings')
    filter_horizontal = ('categories',)  # nice widget for categories

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    search_fields = ['name']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    search_fields = ['category_name']

# Optionally, you can unregister the RecipeIngredient from the main admin list
# because it is managed inside Recipe:
admin.site.unregister(RecipeIngredient) if admin.site.is_registered(RecipeIngredient) else None
