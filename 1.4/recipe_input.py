import pickle

def take_recipe():
    name = input("Enter the recipe name: ").strip()
    if not name:
        print("Recipe name cannot be empty.")
        return None
    try:
        cooking_time = int(input("Enter the cooking time in minutes: ").strip())
        if cooking_time < 0:
            print("Invalid cooking time.")
            return None
    except ValueError:
        print("Invalid cooking time.")
        return None

    ingredients_input = input("Enter the ingredients, separated by commas. Use quotes for ingredients with spaces: ")
    ingredients = [i.strip().lower() for i in ingredients_input.split(',')]
    if not all(ingredients):
        print("Invalid ingredients.")
        return None

    difficulty = calc_difficulty(cooking_time, len(ingredients))
    return {'name': name, 'time': cooking_time, 'ingredients': ingredients, 'difficulty': difficulty}

def calc_difficulty(time, num_ingredients):
    if time < 10:
        if num_ingredients < 4:
            return "Easy"
        else:
            return "Medium"
    else:
        if num_ingredients < 4:
            return "Intermediate"
        else:
            return "Hard"

filename = input("Enter the filename to store recipes: ")

try:
    with open(filename, 'rb') as f:
        data = pickle.load(f)
except FileNotFoundError:
    data = {'recipes_list': [], 'all_ingredients': []}
except Exception as e:
    print(f"An error occurred: {e}")
    data = {'recipes_list': [], 'all_ingredients': []}

try:
    num_recipes = int(input("How many recipes would you like to enter? "))
except ValueError:
    print("Please enter a valid integer.")
    exit()

for _ in range(num_recipes):
    recipe = take_recipe()
    if recipe is not None:
        data['recipes_list'].append(recipe)
        for ingredient in recipe['ingredients']:
            if ingredient not in data['all_ingredients']:
                data['all_ingredients'].append(ingredient)

try:
    with open(filename, 'wb') as f:
        pickle.dump(data, f)
except Exception as e:
    print(f"An error occurred while saving: {e}")
else:
    print("Recipes saved successfully!")
