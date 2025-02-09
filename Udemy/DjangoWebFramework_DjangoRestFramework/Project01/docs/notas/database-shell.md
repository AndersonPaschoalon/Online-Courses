# Quary single object

recipe = Recipe.objects.get(id=1)
print(recipe)

# Query all recipes

all_recipes = Recipe.objects.all()

