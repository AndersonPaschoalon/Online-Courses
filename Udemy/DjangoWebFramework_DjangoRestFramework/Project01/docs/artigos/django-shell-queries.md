# Django Shell Queries

In Django, you can interact with your database using the Django ORM (Object-Relational Mapper). If you have a model named Recipe, here's how you can retrieve a single recipe and query all recipes from your local database.


## 1. Retrieve a Single Recipe
To retrieve a single recipe, you can use the get() method. This method is used when you expect only one result. If multiple recipes match the query or no recipe is found, it will raise an exception (MultipleObjectsReturned or DoesNotExist).

Example:
```python
# Retrieve a single recipe by its primary key (id)
recipe = Recipe.objects.get(id=1)
```

#### Retrieve a single recipe by another unique field (e.g., name)
recipe = Recipe.objects.get(name="Pasta Carbonara")
Handling Exceptions:
If you're unsure whether the recipe exists, you can handle exceptions:

```python
from django.core.exceptions import ObjectDoesNotExist

try:
    recipe = Recipe.objects.get(id=1)
    print(recipe.name)
except ObjectDoesNotExist:
    print("Recipe not found.")
```


## 2. Query All Recipes
To retrieve all recipes from the database, use the all() method.

Example:
```python
# Retrieve all recipes
all_recipes = Recipe.objects.all()
```

#### Iterate over the recipes
```python
for recipe in all_recipes:
    print(recipe.name)
```


## 3. Filter Recipes
If you want to filter recipes based on certain conditions, use the filter() method.

Example:
```python
# Retrieve all recipes with a specific category
italian_recipes = Recipe.objects.filter(category="Italian")
```

#### Retrieve all recipes with a rating greater than 4
high_rated_recipes = Recipe.objects.filter(rating__gt=4)


# 4. Using the Django Shell
You can test these queries in the Django shell:

```bash
python manage.py shell
```

Then, run your queries:

```python
from myapp.models import Recipe  # Replace 'myapp' with your app name

# Retrieve a single recipe
recipe = Recipe.objects.get(id=1)
print(recipe.name)

# Retrieve all recipes
all_recipes = Recipe.objects.all()
for recipe in all_recipes:
    print(recipe.name)
```

# 5. Example Model
Here’s an example of what your Recipe model might look like:

```python
from django.db import models

class Recipe(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return self.name
```

# 6. Common Query Methods
Here are some common methods you can use with Django ORM:

get(): Retrieve a single object.

all(): Retrieve all objects.

filter(): Retrieve objects matching specific conditions.

exclude(): Exclude objects matching specific conditions.

order_by(): Sort the results.

count(): Get the number of objects.

first(): Get the first object in the queryset.

last(): Get the last object in the queryset.

Examples:
```python
# Get the number of recipes
recipe_count = Recipe.objects.count()

# Get the first recipe
first_recipe = Recipe.objects.first()

# Get the last recipe
last_recipe = Recipe.objects.last()

# Order recipes by name
sorted_recipes = Recipe.objects.all().order_by('name')
```

