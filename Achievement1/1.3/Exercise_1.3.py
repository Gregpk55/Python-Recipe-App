recipes_list = []
ingredients_list = []

def take_recipe():
    name = input("Enter recipe name: ")
    cooking_time = int(input("Enter cooking time (in minutes): "))
    ingredients = [i.strip() for i in input("Enter ingredients separated by commas: ").split(",")]

    recipe = {'name': name, 'cooking_time': cooking_time, 'ingredients': ingredients}
    return recipe


def main():
    n = int(input("How many recipes would you like to enter? "))
    print("----------------------") 

    for _ in range(n):
        recipe = take_recipe()
        for ingredient in recipe['ingredients']:
            if ingredient not in ingredients_list:
                ingredients_list.append(ingredient)
        
        recipes_list.append(recipe)
    
    
    for recipe in recipes_list:
        if recipe['cooking_time'] < 10 and len(recipe['ingredients']) < 4:
            difficulty = "Easy"
        elif recipe['cooking_time'] < 10 and len(recipe['ingredients']) >= 4:
            difficulty = "Medium"
        elif recipe['cooking_time'] >= 10 and len(recipe['ingredients']) < 4:
            difficulty = "Intermediate"
        else:
            difficulty = "Hard"
        
        print("Recipe Name:", recipe['name'])
        print("Cooking Time:", recipe['cooking_time'], "min")
        print("Ingredients:")
        for ingredient in recipe['ingredients']:
            print('  -', ingredient)
        print('Difficulty Level:', difficulty)
        print("----------------------") 
        

    print("\nIngredients across all recipes (in alphabetical order):\n")
    for ingredient in sorted(ingredients_list):
        print('-', ingredient)

if __name__ == "__main__":
    main()
