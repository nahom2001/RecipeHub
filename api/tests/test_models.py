from django.test import TestCase
from api.models import Recipe, User, Category, Ingredient, RecipeIngredient
from datetime import timedelta

class TestModels(TestCase):
    def setUp(self):
        # runs before each test
        self.user = User.objects.create_user(username='testuser', password='fakepassword')
        self.category = Category.objects.create(category_name='Test Category')
        self.ingredient = Ingredient.objects.create(name='pasta')

    def test_model_Recipe(self):
        # Create the Recipe instance
        recipe = Recipe.objects.create(
            title='Test Recipe',
            description='Good recipe',
            instructions='1 heat the pan \n 2, Work it',
            prep_time=timedelta(hours=0, minutes=10),
            cooking_time=timedelta(hours=0, minutes=14),
            servings=4,
            user=self.user
        )

        # Create the RecipeIngredient instance
        recipe_ingredient = RecipeIngredient.objects.create(
            recipe=recipe,
            ingredient=self.ingredient,
            quantity=200,  # Set the quantity
            unit='grams'   # Set the unit
        )

        # Set the category
        recipe.categories.set([self.category])

        # Assertions
        self.assertEqual(str(recipe), 'Test Recipe')
        self.assertTrue(isinstance(recipe, Recipe))
        self.assertIn(self.category, recipe.categories.all())  # Check if category is set
        self.assertIn(self.ingredient, recipe.ingredients.all())  # Check if ingredient is set