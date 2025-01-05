from django.shortcuts import render
from django.http import HttpResponse
from utils.recipes.DummyRecipes import DummyRecipes
from recipes.models import Recipe


#def home(request):
#    return render(request, 'recipes/pages/home.html', context={
#        'recipes': [DummyRecipes().make_recipe() for _ in range(10)],
#    })
def home(request):
    recipes = Recipe.objects.filter(is_published=True).order_by('-id')
    return render(request, 'recipes/pages/home.html', context={
        'recipes': recipes,
    })


def category(request, category_id):
    recipes = Recipe.objects.filter(is_published=True, category__id=category_id).order_by('-id')
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes.first().category.name}' 
    })


#def recipe(request, id):
#    return render(request, 'recipes/pages/recipe-view.html', context={
#        'recipe': DummyRecipes().make_recipe(),
#        'is_detail_page': True,
#    })
def recipe(request, id):
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': DummyRecipes().make_recipe(),
        'is_detail_page': True,
    })