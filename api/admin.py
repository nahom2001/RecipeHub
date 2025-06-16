# your_app_name/admin.py (e.g., api/admin.py)
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin # Import Django's default UserAdmin
# Import your custom User model
from .models import User # Assuming your custom User model is in models.py of the same app

# Now, define your CustomUserAdmin by inheriting from BaseUserAdmin
class CustomUserAdmin(BaseUserAdmin):
    # If you later add custom fields to your User model (e.g., bio, phone_number),
    # you would add them to the 'fieldsets' and 'add_fieldsets' here.
    # For now, by inheriting from BaseUserAdmin, it brings in all the standard
    # user fields, including the password and confirmation fields.
    pass # No need to override anything if you just want default AbstractUser behavior

# Finally, register your custom User model with your CustomUserAdmin
admin.site.register(User, CustomUserAdmin)

# Register your other models as usual:
from .models import Recipe, Ingredient, Category, RecipeIngredient

admin.site.register(Recipe)
admin.site.register(Ingredient)
admin.site.register(Category)
admin.site.register(RecipeIngredient)