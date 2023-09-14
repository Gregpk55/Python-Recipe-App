class Recipe:
    all_ingredients = set()

    def __init__(self, name):
        if not name:
            raise ValueError("Recipe name cannot be empty")
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None

    def get_name(self):
        return self.name

    def set_name(self, new_name):
        if not new_name:
            raise ValueError("Recipe name cannot be empty")
        self.name = new_name

    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, new_time):
        if new_time < 0:
            raise ValueError("Cooking time cannot be negative")
        self.cooking_time = new_time
        self.calculate_difficulty()

    def add_ingredients(self, *args):
        for arg in args:
            if not arg or arg.lower() in [ing.lower() for ing in self.ingredients]:
                continue  
            self.ingredients.append(arg)
        self.update_all_ingredients()

    def get_ingredients(self):
        return self.ingredients

    def calculate_difficulty(self):
        self.difficulty = "Easy" if self.cooking_time < 10 and len(self.ingredients) < 4 else \
                          "Medium" if self.cooking_time < 10 and len(self.ingredients) >= 4 else \
                          "Intermediate" if self.cooking_time >= 10 and len(self.ingredients) < 4 else \
                          "Hard"

    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty

    def search_ingredient(self, ingredient):
        return ingredient in self.ingredients

    def update_all_ingredients(self):
        Recipe.all_ingredients.update(self.ingredients)

    def __str__(self):
        return f"Recipe Name: {self.name}\nIngredients: {', '.join(self.ingredients)}\nCooking Time: {self.cooking_time} minutes\nDifficulty: {self.get_difficulty()}\n"


def recipe_search(data, search_term):
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)
            print('-' * 20)

recipes_list = []

try:
    tea = Recipe("Tea")
    tea.add_ingredients("Tea Leaves", "Sugar", "Water")
    tea.set_cooking_time(5)
    recipes_list.append(tea)

    coffee = Recipe("Coffee")
    coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
    coffee.set_cooking_time(5)
    recipes_list.append(coffee)

    cake = Recipe("Cake")
    cake.add_ingredients("Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk")
    cake.set_cooking_time(50)
    recipes_list.append(cake)

    banana_smoothie = Recipe("Banana Smoothie")
    banana_smoothie.add_ingredients("Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
    banana_smoothie.set_cooking_time(5)
    recipes_list.append(banana_smoothie)
except ValueError as ve:
    print(ve)

print('-' * 20)
print("Recipes containing Water:")
recipe_search(recipes_list, "Water")


print("Recipes containing Sugar:")
recipe_search(recipes_list, "Sugar")


print("Recipes containing Bananas:")
recipe_search(recipes_list, "Bananas")
