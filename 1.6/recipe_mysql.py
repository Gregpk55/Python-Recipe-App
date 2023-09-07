import mysql.connector


conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password'
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    ingredients VARCHAR(255),
    cooking_time INT,
    difficulty VARCHAR(20)
)
""")


def main_menu(conn, cursor):
    print("-" * 20)
    print("Main Menu")
    print("-" * 20)
    while True:
        print("\n1. Create Recipe")
        print("2. Search Recipe")
        print("3. Update Recipe")
        print("4. Delete Recipe")
        print("5. Exit")
        
        choice = input("Choose an option: ")
        
        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5':
            print("Exiting...")
            conn.close()
            break
        else:
            print("Invalid choice. Try again.")



def calculate_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients.split(", ")) < 4:
        return "Easy"
    elif cooking_time < 10 and len(ingredients.split(", ")) >= 4:
        return "Medium"
    elif cooking_time >= 10 and len(ingredients.split(", ")) < 4:
        return "Intermediate"
    else:
        return "Hard"
    
# create
def create_recipe(conn, cursor):
    try:
        print("-" * 20)
        print("Create Recipe")
        print("-" * 20)
        name = input("Enter recipe name: ")
        cooking_time = int(input("Enter cooking time in minutes: "))
        ingredients = input("Enter ingredients separated by commas: ")
        ingredients = ", ".join(ingredient.strip().lower() for ingredient in ingredients.split(", "))
        difficulty = calculate_difficulty(cooking_time, ingredients)

        query = "INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s);"
        cursor.execute(query, (name, ingredients, cooking_time, difficulty))
        conn.commit()
    except Exception as e:
         print(f"Could not create '{name}'. An error occurred: {e}")


# search
def search_recipe(conn, cursor):
    try:
        print("-" * 20)
        print("Search Recipe")
        print("-" * 20)
        
        cursor.execute("SELECT ingredients FROM Recipes;")
        results = cursor.fetchall()
        
        if not results:
            print("No ingredients found in any recipes.")
            return

        all_ingredients = set()
        for row in results:
            ingredients = row[0].split(", ")
            all_ingredients.update(ingredients)
        
        print("Available ingredients:")
        for idx, ingredient in enumerate(sorted(all_ingredients)):
            print(f"{idx + 1}. {ingredient}")

        choice = int(input("Choose an ingredient to search for: "))
        search_ingredient = sorted(all_ingredients)[choice - 1]

        cursor.execute(f"SELECT * FROM Recipes WHERE ingredients LIKE %s", (f"%{search_ingredient}%",))
        matching_recipes = cursor.fetchall()
        
        
        if not matching_recipes:
            print(f"No recipes found containing the ingredient: {search_ingredient}")
            return

        print("Recipes containing that ingredient:")
        for recipe in matching_recipes:
            print("\n---------------------")
            print(f"Name: {recipe[1]}")
            print(f"Ingredients: {recipe[2]}")
            print(f"Cooking Time: {recipe[3]} minutes")
            print(f"Difficulty: {recipe[4]}")
            
    except Exception as e:
        print(f"Could not search. An error occurred: {e}")


# Update
def update_recipe(conn, cursor):
    try:
        print("-" * 20)
        print("Update Recipe")
        print("-" * 20)
        
        cursor.execute("SELECT * FROM Recipes;")
        recipes = cursor.fetchall()

        if not recipes:
            print("No recipes available for update.")
            return

        print("Available recipes:")
        for recipe in recipes:
            print("\n---------------------")
            print(f"ID: {recipe[0]}")
            print(f"Name: {recipe[1]}")
            print(f"Ingredients: {recipe[2]}")
            print(f"Cooking Time: {recipe[3]} minutes")
            print(f"Difficulty: {recipe[4]}")
        
        choice = int(input("\nChoose a recipe id to update: "))
        
        cursor.execute("SELECT COUNT(*) FROM Recipes WHERE id = %s", (choice,))
        exists = cursor.fetchone()[0]

        if exists == 0:
            print("Recipe with this id does not exist.")
            return

        print("\nWhich column would you like to update?")
        print("1. Name")
        print("2. Cooking Time")
        print("3. Ingredients")
        
        column_choice = input("Choose an option: ")

        new_value = input("Enter the new value: ")

        if column_choice == '1':
            column_to_update = 'name'
        elif column_choice == '2':
            column_to_update = 'cooking_time'
        elif column_choice == '3':
            column_to_update = 'ingredients'
            new_value = ", ".join(ingredient.strip().lower() for ingredient in new_value.split(", "))
        else:
            print("Invalid choice.")
            return

        query = f"UPDATE Recipes SET {column_to_update} = %s WHERE id = %s;"
        cursor.execute(query, (new_value, choice))
        
        conn.commit()
        
    except Exception as e:
        print(f"Could not update. An error occurred: {e}")


# delete
def delete_recipe(conn, cursor):
    try:
        print("-" * 20)
        print("Delete Recipe")
        print("-" * 20)
        
        cursor.execute("SELECT * FROM Recipes;")
        recipes = cursor.fetchall()

        if not recipes:
            print("No recipes available for deletion.")
            return

        print("Available recipes:")
        for recipe in recipes:
            print(recipe)
        
        choice = int(input("Choose a recipe id to delete: "))

        cursor.execute("SELECT COUNT(*) FROM Recipes WHERE id = %s", (choice,))
        exists = cursor.fetchone()[0]

        if exists == 0:
            print("Recipe with this id does not exist.")
            return

        cursor.execute("SELECT name FROM Recipes WHERE id = %s", (choice,))
        recipe_name = cursor.fetchone()[0]
        
        query = "DELETE FROM Recipes WHERE id = %s;"
        cursor.execute(query, (choice,))
        conn.commit()
        
        print(f'The recipe "{recipe_name}" has been deleted.')
        
    except Exception as e:
        print(f"Could not delete. An error occurred: {e}")

if __name__ == "__main__":
    main_menu(conn, cursor)
    conn.close()