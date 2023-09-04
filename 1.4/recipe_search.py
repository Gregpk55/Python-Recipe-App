import pickle

def display_recipe(recipe):
    print(f"Recipe Name: {recipe['name']}")
    print(f"Cooking Time: {recipe['time']} minutes")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {recipe['difficulty']}")
    print()

def search_ingredient(data):
    all_ingredients = data.get('all_ingredients', [])
    if not all_ingredients:
        print("No ingredients found.")
        return
    for i, ingredient in enumerate(all_ingredients):
        print(f"{i+1}. {ingredient}")

    try:
        choice = int(input("Pick a number to search for an ingredient (or enter 0 to exit): "))
        if choice == 0:
            return
        ingredient_searched = all_ingredients[choice - 1]
    except (ValueError, IndexError, KeyboardInterrupt):
        print("Incorrect input. Exiting...")
        return

    found_recipes = [recipe for recipe in data['recipes_list'] if ingredient_searched in recipe.get('ingredients', [])]

    print(f"Found {len(found_recipes)} recipe(s) with {ingredient_searched}:")
    for recipe in found_recipes:
        display_recipe(recipe)

try:
    filename = input("Enter the filename where the recipes are stored: ") 
    with open(filename, 'rb') as f:
        data = pickle.load(f)
except FileNotFoundError:
    print("File doesn't exist - exiting.")
except Exception as e:
    print(f"An error occurred: {e}")
else:
    search_ingredient(data)
