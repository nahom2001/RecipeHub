from rest_framework import serializers
from .models import Recipe, Ingredient, RecipeIngredient, Category

class RecipeSummarySerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        slug_field='category_name',
        read_only=True
    )

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'prep_time', 'cooking_time', 'servings', 'categories']


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['id', 'name']

class RecipeIngredientSerializer(serializers.ModelSerializer):
    ingredient = IngredientSerializer()

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'unit']

class RecipeSerializer(serializers.ModelSerializer):
    categories = serializers.SlugRelatedField(
        many=True,
        slug_field='category_name',
        queryset=Category.objects.all()
    )
    recipe_ingredients = RecipeIngredientSerializer(source='recipeingredient_set', many=True)

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'description', 'instructions', 'prep_time', 'cooking_time', 'servings', 'categories', 'recipe_ingredients']

    def create(self, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')
        recipe = Recipe.objects.create(**validated_data)
        for item in ingredients_data:
            ingredient_data = item.pop('ingredient')
            ingredient, created = Ingredient.objects.get_or_create(**ingredient_data)
            RecipeIngredient.objects.create(recipe=recipe, ingredient=ingredient, **item)
        return recipe

    def update(self, instance, validated_data):
        ingredients_data = validated_data.pop('recipeingredient_set')
        # Update recipe fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update ingredients - simple approach: delete all and re-create
        instance.recipeingredient_set.all().delete()
        for item in ingredients_data:
            ingredient_data = item.pop('ingredient')
            ingredient, created = Ingredient.objects.get_or_create(**ingredient_data)
            RecipeIngredient.objects.create(recipe=instance, ingredient=ingredient, **item)

        return instance
