class ShoppingList:
    def __init__(self, list_name):
        self.list_name = list_name
        self.shopping_list = []

    def add_item(self, item):
        if item not in self.shopping_list:
            self.shopping_list.append(item)
            print(f"Added {item} to list")
        else:
            print(f"{item} already in list")

    def remove_item(self, item):
        if item in self.shopping_list:
            self.shopping_list.remove(item)
            print(f"{item} is removed")
        else:
            print(f"This {item} is not in the list")

    def view_list(self):
        print(f"{self.list_name} conatins:")
        for item in self.shopping_list:
            print(f"- {item}")

pet_store_list = ShoppingList("Pet shopping list")

pet_store_list.add_item("dog food")
pet_store_list.add_item("frisbee")
pet_store_list.add_item("bowl")
pet_store_list.add_item("collar")
pet_store_list.add_item("flea collar")

pet_store_list.remove_item("flea collar")

pet_store_list.add_item("frisbee")

pet_store_list.view_list()