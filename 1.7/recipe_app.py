
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.types import Integer, String
from sqlalchemy import Column
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine

engine = create_engine("mysql://cf-python:password@localhost/my_database")

Base = declarative_base()

Session = sessionmaker(bind=engine)

class Recipe(Base):
    __tablename__ = 'final_recipes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        return f"<Recipe {self.id} - {self.name} ({self.difficulty})>"

    def __str__(self):
        return (f"\nRecipe: {self.name}\nIngredients: {self.ingredients}\n"
                f"Cooking Time: {self.cooking_time} mins\n"
                f"Difficulty: {self.difficulty}\n")

    def calculate_difficulty(self):
        ingredient_count = len(self.return_ingredients_as_list())
        if self.cooking_time < 10 and ingredient_count < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and ingredient_count >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and ingredient_count < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"

    def return_ingredients_as_list(self):
        return [] if not self.ingredients else self.ingredients.split(', ')

Base.metadata.create_all(engine)


# Create
def create_recipe(session):
    print("\n" + "-"*20)
    name = input("Enter recipe name (max 50 chars): ").strip()
    if not 0 < len(name) <= 50 or not all(char.isalpha() or char.isspace() for char in name):
        print("Invalid input!")
        return

    ingredients_list = []
    while True:
        try:
            ingredient_count = int(input("How many ingredients? "))
            if ingredient_count <= 0:
                print("Please enter a valid positive number of ingredients.")
                continue
            break
        except ValueError:
            print("Please enter a valid number.")

    for _ in range(ingredient_count):
        ingredient = input(f"Enter ingredients {_ + 1}: ").strip()
        ingredients_list.append(ingredient)
    ingredients = ', '.join(ingredients_list)
    
    while True:
        try:
            cooking_time = int(input("Enter cooking time in minutes: "))
            break
        except ValueError:
            print("Please enter a valid number for cooking time.")

    recipe_entry = Recipe(name=name, ingredients=ingredients, cooking_time=cooking_time)
    recipe_entry.calculate_difficulty()
    session.add(recipe_entry)
    session.commit()

    print(f"{recipe_entry.name} has been added to the recipe list.")
    print("-"*20)


# View all
def view_all_recipes(session):
    print("\n" + "-"*20)
    recipes = session.query(Recipe).all()
    
    print("\nAll Recipes")
    print("-" * 20)
    
    if not recipes:
        print("No recipes found!")
        return

    for recipe in recipes:
        print(recipe)
        print("-" * 20)


# Search
def search_by_ingredients(session):
    print("\n" + "-"*20)
    if session.query(Recipe).count() == 0:
        print("No recipes found in the database!")
        return

    results = session.query(Recipe.ingredients).all()

    all_ingredients = []
    for entry in results:
        ing_list = entry[0].split(', ')
        for ing in ing_list:
            if ing not in all_ingredients:
                all_ingredients.append(ing)

    print("Available ingredients:")
    for idx, ingredient in enumerate(all_ingredients, 1):
        print(f"{idx}. {ingredient}")

    try:
        selected_numbers = list(map(int, input("Enter the number of the ingredient: ").split(',')))
        search_ingredients = [all_ingredients[num - 1] for num in selected_numbers]
    except (ValueError, IndexError):
        print("Invalid input. Please select from the given ingredient numbers.")
        return
    conditions = [Recipe.ingredients.like(f"%{ing}%") for ing in search_ingredients]
    recipes = session.query(Recipe).filter(*conditions).all()
    if not recipes:
        print("No recipes match your selected ingredients.")
        return

    for recipe in recipes:
        print(recipe)


# Edit
def edit_recipe(session):
    print("\n" + "-"*20)
    recipes = session.query(Recipe).all()
    
    if not recipes:
        print("No recipes available to edit.")
        return

    for idx, recipe in enumerate(recipes, 1):
        print(f"{idx}. {recipe.name}")
    print("\n" + "-"*20)

    while True:
        try:
            choice_idx = int(input("\nEnter the number of the recipe you'd like to edit: "))
            if 1 <= choice_idx <= len(recipes):
                recipe_to_edit = recipes[choice_idx - 1]
                break
            else:
                print("Choice out of range. Please select a valid recipe number.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    print("1. Name: ", recipe_to_edit.name)
    print("2. Ingredients: ", recipe_to_edit.ingredients)
    print("3. Cooking Time: ", recipe_to_edit.cooking_time)

    choice = input("\nEnter the number corresponding to the attribute you'd like to edit: ")

    if choice == "1":
        new_name = input("Enter the new name (max 50 characters): ").strip()
        if 0 < len(new_name) <= 50 and all(char.isalpha() or char.isspace() for char in new_name):
            recipe_to_edit.name = new_name
        else:
            print("Invalid name input. Edit aborted.")
            return

    elif choice == "2":
        print("Ingredients options:")
        print("1. Overwrite the entire list of ingredients")
        print("2. Add ingredients to the current list")
        print("-"*20)
        sub_choice = input("Enter your choice: ")

        if sub_choice == "1":
            while True:
                try:
                    ingredients_count = int(input("How many ingredients would you like to enter? "))
                    break
                except ValueError:
                    print("Please enter a valid number.")

            ingredients_list = []
            for i in range(ingredients_count):
                while True:
                    ingredient = input(f"Enter ingredient {i + 1}: ").strip()
                    if not ingredient.replace('.', '', 1).isnumeric():
                        ingredients_list.append(ingredient)
                        break
                    else:
                        print("Invalid ingredient. Ingredients shouldn't be just numbers.")

            recipe_to_edit.ingredients = ', '.join(ingredients_list)

        elif sub_choice == "2":
            while True:
                try:
                    ingredients_count = int(input("How many ingredients would you like to add? "))
                    break
                except ValueError:
                    print("Please enter a valid number.")

            current_ingredients = recipe_to_edit.ingredients.split(', ')
            for i in range(ingredients_count):
                while True:
                    ingredient = input(f"Enter ingredient to add {i + 1}: ").strip()
                    if not ingredient.replace('.', '', 1).isnumeric():
                        current_ingredients.append(ingredient)
                        break
                    else:
                        print("Invalid ingredient. Ingredients shouldn't be just numbers.")
            recipe_to_edit.ingredients = ', '.join(current_ingredients)
            print(f"Ingredients have been added to the recipe!")

        else:
            print("Invalid choice. Edit aborted.")
            return

    elif choice == "3":
        while True:
            new_time = input("Enter the new cooking time (in minutes): ").strip()
            if new_time.isnumeric():
                recipe_to_edit.cooking_time = int(new_time)
                break
            else:
                print("Invalid input. Cooking time must be a number.")

    else:
        print("Invalid choice. Edit aborted.")
        return

    recipe_to_edit.calculate_difficulty()
    session.commit()
    print(f"\n{recipe_to_edit.name} has been updated!" "\n" + "-"*20)



# Delete
def delete_recipe(session):
    print("\n" + "-"*20)
    recipe_count = session.query(Recipe).count()
    if recipe_count == 0:
        print("No recipes available to delete.")
        return

    results = session.query(Recipe.id, Recipe.name).all()

    for recipe in results:
        print(f"{recipe.id}. {recipe.name}")

    recipe_id = input("Enter the ID of the recipe you'd like to delete: ")

    if not recipe_id.isnumeric():
        print("Invalid input. Exiting delete function.")
        return

    recipe_id = int(recipe_id)

    try:
        recipe_to_delete = session.query(Recipe).filter_by(id=recipe_id).one()
    except NoResultFound:
        print("Recipe not found. Exiting delete function.")
        return

    while True:
        confirm = input(f"Are you sure you want to delete {recipe_to_delete.name}? (yes/no): ").strip().lower()
        if confirm in ["yes", "no"]:
            break
        print("Please enter 'yes' or 'no'.")
        
    if confirm == 'yes':
        session.delete(recipe_to_delete)
        session.commit()
        print(f"{recipe_to_delete.name} has been deleted successfully!")
    else:
        print("Deletion aborted.")


operations = {
    '1': {
        'function': create_recipe,
        'description': 'Create Recipe'
    },
    '2': {
        'function': view_all_recipes,
        'description': 'View All Recipes'
    },
    '3': {
        'function': search_by_ingredients,
        'description': 'Search by Ingredients'
    },
    '4': {
        'function': edit_recipe,
        'description': 'Edit Recipe'
    },
    '5': {
        'function': delete_recipe,
        'description': 'Delete Recipe'
    }
}

def main():
    session = Session()
    while True:
        print("\nRecipe Management System")
        print("-" * 20)
        for key, value in operations.items():
            print(f"{key}. {value['description']}")
        print("6. Exit")
        print("-" * 20)
        
        choice = input("\nEnter your choice: ")

        if choice in operations:
            operations[choice]['function'](session)
        elif choice == '6':
            print("\nExiting...")
            break
        else:
            print("\nInvalid choice. Please try again.")
            
    session.close()
    engine.dispose()

if __name__ == "__main__":
    main()