from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination
from .serializers import RecipeSerializer, RecipeSummarySerializer, CategorySerializer
from django.contrib.auth.decorators import login_required

from .models import Recipe, Category, Ingredient
from django.db.models import Q

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

from .utils import filter_recipes, paginate_queryset

# Swagger import
from drf_yasg.utils import swagger_auto_schema


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username

        return token
    
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


@api_view(['GET'])
def api_menu(request):
    api_urls = {
        'List': '/recipe-list/',
        'Detail View': '/recipe-detail/<str:pk>/',
        'Create': '/recipe-create/',
        'Update': '/recipe-update/<str:pk>/',
        'Delete': '/recipe-delete/<str:pk>/'
    }
    return Response(api_urls)


@api_view(['GET'])
def recipe_list(request):
    recipes = Recipe.objects.all()
    filtered_recipes = filter_recipes(recipes, request.GET)
    paginated_recipes, paginator = paginate_queryset(filtered_recipes, request)
    serializer = RecipeSummarySerializer(paginated_recipes, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recipe_detail(request, pk):
    recipes = Recipe.objects.get(id=pk)
    serializer = RecipeSerializer(recipes, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def recipe_category(request, category_name):
    try:
        category = Category.objects.get(category_name__iexact=category_name)
    except Category.DoesNotExist:
        return Response({"detail": "Category not found."}, status=404)

    recipes = category.recipes.all()
    serializer = RecipeSerializer(recipes, many=True)

    return Response({
        "category": {
            "name": category.category_name
        },
        "recipes": serializer.data
    })


@api_view(['GET'])
def recipe_ingredient(request, ingredient):
    try:
        ingredients = Ingredient.objects.filter(name__icontains=ingredient)
    except Ingredient.DoesNotExist:
        return Response({"detail": "Ingredient not found."}, status=404)

    recipes = Recipe.objects.filter(recipeingredient__ingredient__in=ingredients).distinct()
    serializer = RecipeSerializer(recipes, many=True)

    return Response({
        "ingredient": {
            "query": ingredient,
            "matched": [ing.name for ing in ingredients]
        },
        "recipes": serializer.data
    })


@swagger_auto_schema(method='post', request_body=RecipeSerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recipe_create(request):
    serializer = RecipeSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='post', request_body=CategorySerializer)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def category_create(request):
    serializer = CategorySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()  
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(method='post', request_body=RecipeSerializer)
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def recipe_update(request, pk):
    recipe = Recipe.objects.get(id=pk)

    if recipe.user != request.user:
        return Response({'detail': 'You do not have permission to update this recipe.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = RecipeSerializer(instance=recipe, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticated])
def recipe_delete(request, pk):
    recipe = Recipe.objects.get(id=pk)

    if recipe.user != request.user:
        return Response({'detail': 'You do not have permission to update this recipe.'}, status=status.HTTP_403_FORBIDDEN)

    recipe.delete()

    return Response('Recipe successfully deleted!')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def search(request):
    pass
