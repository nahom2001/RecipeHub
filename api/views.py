from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from rest_framework.pagination import PageNumberPagination
from .serializers import RecipeSerializer
from django.contrib.auth.decorators import login_required

# Create your views here.
from .models import Recipe
from django.db.models import Q

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# auth imports
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

# importing custom utilities

from .utils import filter_recipes, paginate_queryset

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        #Add custom claims
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
    serializer = RecipeSerializer(paginated_recipes, many=True)
    return paginator.get_paginated_response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def recipe_detail(request, pk):
    recipes = Recipe.objects.get(id=pk)
    serializer = RecipeSerializer(recipes, many=False)
    return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def recipe_create(request):
    serializer = RecipeSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def recipe_update(request, pk):
    recipe = Recipe.objects.get(id=pk)

    if recipe.user != request.user:
        return Response({'detail': 'You do not have permission to update this recipe.'}, status=status.HTTP_403_FORBIDDEN)

    serializer = RecipeSerializer(instance=recipe, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
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
    