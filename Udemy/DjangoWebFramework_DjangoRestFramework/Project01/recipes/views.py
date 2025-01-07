from django.http import Http404
from django.shortcuts import render, get_list_or_404, get_object_or_404
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
    recipes = get_list_or_404(
        Recipe.objects.filter(
            category__id=category_id,
            is_published=True,
        ).order_by('-id')
    )
    return render(request, 'recipes/pages/category.html', context={
        'recipes': recipes,
        'title': f'{recipes[0].category.name}',
    })



#def recipe(request, id):
#    return render(request, 'recipes/pages/recipe-view.html', context={
#        'recipe': DummyRecipes().make_recipe(),
#        'is_detail_page': True,
#    })
def recipe(request, id):
    recipe = get_object_or_404(Recipe, pk=id, is_published=True,)
    return render(request, 'recipes/pages/recipe-view.html', context={
        'recipe': recipe,
        'is_detail_page': True,
    })