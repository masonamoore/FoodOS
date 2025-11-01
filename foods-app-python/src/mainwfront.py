import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import mysql.connector
import csv

# Make Connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="cpsc408!",
    database="Final_Schema",
    auth_plugin='mysql_native_password'
)

# Create cursor object
cur_obj = conn.cursor(buffered=True)

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Foods App")
        self.create_main_menu()

    #This creates all of the buttons you need to be able to work through the application
    def create_main_menu(self):
        frame = ttk.Frame(self.root, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Welcome to Foods! Please select an option:").grid(column=0, row=0, columnspan=2, pady=10)

        ttk.Button(frame, text="Meal Plan", command=self.meal_plan).grid(column=0, row=1, sticky=(tk.W, tk.E), pady=5, padx=10)
        ttk.Button(frame, text="Grocery List", command=self.grocery_list).grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5, padx=10)
        ttk.Button(frame, text="Recipes", command=self.recipes).grid(column=0, row=2, sticky=(tk.W, tk.E), pady=5, padx=10)
        ttk.Button(frame, text="Inventory", command=self.inventory).grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5, padx=10)
        ttk.Button(frame, text="Updates", command=self.updates).grid(column=0, row=3, sticky=(tk.W, tk.E), pady=5, padx=10)
        ttk.Button(frame, text="Export Meal Plan", command=self.export_meal_plan_to_csv).grid(column=1, row=3, sticky=(tk.W, tk.E), pady=5, padx=10)
        ttk.Button(frame, text="Quit", command=self.quit_app).grid(column=0, row=4, columnspan=2, sticky=(tk.W, tk.E), pady=5, padx=10)
    #This function brins up the meal plan view and has the smaller functions inside 
    #The smaller functions inside are copies of queries from the clp app
    def meal_plan(self):
        def view_meal_plan():
            cur_obj.execute('''
                SELECT MP.MealPlanID, MP.MealDate, R.name AS RecipeName
                FROM MealPlan MP
                JOIN Recipe R ON MP.RecipeID = R.RecipeID
                ORDER BY MP.MealDate;
            ''')
            meal_plan = cur_obj.fetchall()
            listbox.delete(0, tk.END)
            for item in meal_plan:
                listbox.insert(tk.END, item)

        def add_meal():
            meal_date = simpledialog.askstring("Input", "Meal Date (YYYY-MM-DD):")
            recipe_id = simpledialog.askstring("Input", "Recipe ID:")
            sql_query = '''
                INSERT INTO MealPlan (MealDate, RecipeID)
                VALUES (%s, %s);
            '''
            data = (meal_date, recipe_id)
            cur_obj.execute(sql_query, data)
            conn.commit()
            messagebox.showinfo("Info", "New meal added to the meal plan.")

        def update_meal():
            meal_plan_id = simpledialog.askstring("Input", "Meal Plan ID:")
            meal_date = simpledialog.askstring("Input", "New Meal Date (YYYY-MM-DD):")
            recipe_id = simpledialog.askstring("Input", "New Recipe ID:")
            sql_query = '''
                UPDATE MealPlan
                SET MealDate = %s, RecipeID = %s
                WHERE MealPlanID = %s;
            '''
            data = (meal_date, recipe_id, meal_plan_id)
            cur_obj.execute(sql_query, data)
            conn.commit()
            messagebox.showinfo("Info", "Meal plan updated.")

        window = tk.Toplevel(self.root)
        window.title("Meal Plan")

        frame = ttk.Frame(window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        listbox = tk.Listbox(frame, width=50, height=20)
        listbox.grid(column=0, row=1, columnspan=4, pady=10)

        ttk.Button(frame, text="View Meal Plan", command=view_meal_plan).grid(column=0, row=0, pady=5, padx=10)
        ttk.Button(frame, text="Add Meal", command=add_meal).grid(column=1, row=0, pady=5, padx=10)
        ttk.Button(frame, text="Update Meal", command=update_meal).grid(column=2, row=0, pady=5, padx=10)

    #Handles grocery list settings see main.py 
    #Also has the same queries from main.py
    def grocery_list(self):
        def view_grocery_list():
            cur_obj.execute('''
                SELECT GL.GroceryListID, I.name, GL.store
                FROM GroceryList GL
                JOIN RecipeIngredient RI ON GL.RecipeIngredientID = RI.RecipeIngredientID
                JOIN Ingredient I ON RI.IngredientID = I.IngredientID;
            ''')
            grocery_list = cur_obj.fetchall()
            listbox.delete(0, tk.END)
            for item in grocery_list:
                listbox.insert(tk.END, item)

        def add_grocery_item():
            ingredient_id = simpledialog.askstring("Input", "Ingredient ID:")
            store = simpledialog.askstring("Input", "Store:")
            cur_obj.execute('''
                SELECT RecipeIngredientID
                FROM RecipeIngredient
                WHERE IngredientID = %s;
            ''', (ingredient_id,))
            recipe_ingredient_id = cur_obj.fetchone()
            if recipe_ingredient_id:
                sql_query = '''
                    INSERT INTO GroceryList (RecipeIngredientID, store)
                    VALUES (%s, %s);
                '''
                data = (recipe_ingredient_id[0], store)
                cur_obj.execute(sql_query, data)
                conn.commit()
                messagebox.showinfo("Info", "Item added to the Grocery List.")
            else:
                messagebox.showerror("Error", "No matching RecipeIngredient found for the provided Ingredient ID.")

        def delete_grocery_item():
            grocery_list_id = simpledialog.askstring("Input", "Grocery List ID:")
            sql_query = '''
                DELETE FROM GroceryList
                WHERE GroceryListID = %s;
            '''
            cur_obj.execute(sql_query, (grocery_list_id,))
            conn.commit()
            messagebox.showinfo("Info", "Item deleted from the Grocery List.")

        window = tk.Toplevel(self.root)
        window.title("Grocery List")

        frame = ttk.Frame(window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        listbox = tk.Listbox(frame, width=50, height=20)
        listbox.grid(column=0, row=1, columnspan=4, pady=10)

        ttk.Button(frame, text="View Grocery List", command=view_grocery_list).grid(column=0, row=0, pady=5, padx=10)
        ttk.Button(frame, text="Add Item", command=add_grocery_item).grid(column=1, row=0, pady=5, padx=10)
        ttk.Button(frame, text="Delete Item", command=delete_grocery_item).grid(column=2, row=0, pady=5, padx=10)

    #This handles all of your recipes 
    #see main.py to explain the queries and show you via the clp app
    def recipes(self):
        def show_recipes(query, params=()):
            cur_obj.execute(query, params)
            recipes = cur_obj.fetchall()
            listbox.delete(0, tk.END)
            for recipe in recipes:
                listbox.insert(tk.END, recipe)

        window = tk.Toplevel(self.root)
        window.title("Recipes")

        frame = ttk.Frame(window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        listbox = tk.Listbox(frame, width=70, height=20)
        listbox.grid(column=0, row=1, columnspan=4, pady=10)
        #These are all the same form main.py and have the same functions
        ttk.Label(frame, text="How do you want to see the recipes sorted?").grid(column=0, row=0, columnspan=4, pady=10)
        ttk.Button(frame, text="Alphabetical", command=lambda: show_recipes("SELECT name, instructions FROM Recipe ORDER BY name")).grid(column=0, row=2, pady=5, padx=10)
        ttk.Button(frame, text="By meal type", command=lambda: self.meal_type_recipes(show_recipes)).grid(column=1, row=2, pady=5, padx=10)
        ttk.Button(frame, text="Cooking time quick", command=lambda: show_recipes("SELECT name, instructions, cookTimeMin FROM Recipe WHERE cookTimeMin <= 15")).grid(column=2, row=2, pady=5, padx=10)
        ttk.Button(frame, text="Cooking time medium", command=lambda: show_recipes("SELECT name, instructions, cookTimeMin FROM Recipe WHERE cookTimeMin > 15 AND cookTimeMin <= 45")).grid(column=3, row=2, pady=5, padx=10)
        ttk.Button(frame, text="Cooking time long", command=lambda: show_recipes("SELECT name, instructions, cookTimeMin FROM Recipe WHERE cookTimeMin > 45")).grid(column=0, row=3, pady=5, padx=10)
        ttk.Button(frame, text="Ingredients available", command=lambda: show_recipes('''
            SELECT DISTINCT R.name
            FROM Recipe R
            JOIN RecipeIngredient RI ON R.RecipeID = RI.RecipeID
            JOIN Inventory I ON RI.IngredientID = I.IngredientID
            WHERE I.quantity > 0;
        ''')).grid(column=1, row=3, pady=5, padx=10)
        ttk.Button(frame, text="Missing few ingredients", command=lambda: self.missing_ingredients_recipes(show_recipes)).grid(column=2, row=3, pady=5, padx=10)
        ttk.Button(frame, text="On this week's meal plan", command=lambda: show_recipes('''
            SELECT R.name
            FROM MealPlan MP
            JOIN Recipe R ON MP.RecipeID = R.RecipeID
            JOIN RecipeIngredient RI ON R.RecipeID = RI.RecipeID
            JOIN Inventory I ON RI.IngredientID = I.IngredientID
            WHERE I.quantity > 0
            GROUP BY R.RecipeID, R.name
            HAVING COUNT(DISTINCT RI.IngredientID) = COUNT(DISTINCT I.IngredientID);
        ''')).grid(column=3, row=3, pady=5, padx=10)
        ttk.Button(frame, text="Low Calorie", command=lambda: show_recipes('''
            SELECT R.name, R.instructions
            FROM Recipe R
            JOIN RecipeIngredient RI ON R.RecipeID = RI.RecipeID
            JOIN Ingredient I ON RI.IngredientID = I.IngredientID
            GROUP BY R.name, R.instructions
            HAVING SUM(I.cal * RI.quantity) <= 300;
        ''')).grid(column=0, row=4, pady=5, padx=10)
        ttk.Button(frame, text="Medium Calorie", command=lambda: show_recipes('''
            SELECT R.name, R.instructions
            FROM Recipe R
            JOIN RecipeIngredient RI ON R.RecipeID = RI.RecipeID
            JOIN Ingredient I ON RI.IngredientID = I.IngredientID
            GROUP BY R.name, R.instructions
            HAVING SUM(I.cal * RI.quantity) > 300 AND SUM(I.cal * RI.quantity) <= 600;
        ''')).grid(column=1, row=4, pady=5, padx=10)
        ttk.Button(frame, text="High Calorie", command=lambda: show_recipes('''
            SELECT R.name, R.instructions
            FROM Recipe R
            JOIN RecipeIngredient RI ON R.RecipeID = RI.RecipeID
            JOIN Ingredient I ON RI.IngredientID = I.IngredientID
            GROUP BY R.name, R.instructions
            HAVING SUM(I.cal * RI.quantity) > 600;
        ''')).grid(column=2, row=4, pady=5, padx=10)

    def meal_type_recipes(self, show_recipes):
        meal_type = simpledialog.askstring("Input", "Specify the meal type (Breakfast, Lunch, Dinner, Snack):")
        show_recipes("SELECT name, instructions FROM Recipe WHERE category = %s ORDER BY name;", (meal_type,))

    def missing_ingredients_recipes(self, show_recipes):
        max_missing = simpledialog.askstring("Input", "Specify the maximum number of missing ingredients:")
        show_recipes('''
            SELECT R.name
            FROM Recipe R
            JOIN RecipeIngredient RI ON R.RecipeID = RI.RecipeID
            LEFT JOIN Inventory I ON RI.IngredientID = I.IngredientID AND I.quantity > 0
            GROUP BY R.RecipeID, R.name
            HAVING COUNT(CASE WHEN I.IngredientID IS NULL THEN 1 END) <= %s;
        ''', (max_missing,))
    #handles all of the inventory needs you have
    #this function uses and references the inventory
    def inventory(self):
        def show_inventory(query, params=()):
            cur_obj.execute(query, params)
            inventory = cur_obj.fetchall()
            listbox.delete(0, tk.END)
            for item in inventory:
                listbox.insert(tk.END, item)

        def change_inventory_status():
            ingredient_id = simpledialog.askstring("Input", "Please tell me the ingredient ID")
            quantity = simpledialog.askstring("Input", "Now tell me the new quantity")
            sql_query = "UPDATE Inventory SET quantity = %s WHERE IngredientID = %s;"
            data = (quantity, ingredient_id)
            cur_obj.execute(sql_query, data)
            conn.commit()
            messagebox.showinfo("Info", "Inventory status updated successfully")

        window = tk.Toplevel(self.root)
        window.title("Inventory")

        frame = ttk.Frame(window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        listbox = tk.Listbox(frame, width=70, height=20)
        listbox.grid(column=0, row=1, columnspan=4, pady=10)

        ttk.Label(frame, text="Display my ingredients:").grid(column=0, row=0, columnspan=4, pady=10)
        ttk.Button(frame, text="All ingredients", command=lambda: show_inventory("""
            SELECT ing.name 
            FROM Inventory inv
            JOIN Ingredient ing ON inv.IngredientID = ing.IngredientID
            WHERE inv.quantity > 0;
        """)).grid(column=0, row=2, pady=5, padx=10)
        ttk.Button(frame, text="Ingredients in fridge", command=lambda: show_inventory("""
            SELECT ing.name 
            FROM Inventory inv
            JOIN Ingredient ing ON inv.IngredientID = ing.IngredientID
            WHERE inv.quantity > 0 AND inv.location = 'fridge';
        """)).grid(column=1, row=2, pady=5, padx=10)
        ttk.Button(frame, text="Ingredients in freezer", command=lambda: show_inventory("""
            SELECT ing.name 
            FROM Inventory inv
            JOIN Ingredient ing ON inv.IngredientID = ing.IngredientID
            WHERE inv.quantity > 0 AND inv.location = 'freezer';
        """)).grid(column=2, row=2, pady=5, padx=10)
        ttk.Button(frame, text="Ingredients in pantry", command=lambda: show_inventory("""
            SELECT ing.name 
            FROM Inventory inv
            JOIN Ingredient ing ON inv.IngredientID = ing.IngredientID
            WHERE inv.quantity > 0 AND inv.location = 'pantry';
        """)).grid(column=3, row=2, pady=5, padx=10)
        ttk.Button(frame, text="Change inventory status", command=change_inventory_status).grid(column=0, row=3, pady=5, padx=10)
    #this handles the updates
    #similar to main.py in terms of all of the functions but translates to tkinter so that you can use
    #in the nicer front end section
    #each definiton below includes the queries you need
    def updates(self):
        def update_ingredients():
            def add_ingredient():
                name = simpledialog.askstring("Input", "Enter name:")
                description = simpledialog.askstring("Input", "Enter description:")
                cal = simpledialog.askstring("Input", "Enter calories:")
                protein = simpledialog.askstring("Input", "Enter protein:")
                fat = simpledialog.askstring("Input", "Enter fat:")
                carb = simpledialog.askstring("Input", "Enter carbs:")
                sql_query = '''
                    INSERT INTO Ingredient (name, description, cal, protein, fat, carb)
                    VALUES (%s, %s, %s, %s, %s, %s);
                '''
                data = (name, description, cal, protein, fat, carb)
                cur_obj.execute(sql_query, data)
                conn.commit()
                messagebox.showinfo("Info", "Ingredient added.")

            def delete_ingredient():
                ingredient_id = simpledialog.askstring("Input", "Enter IngredientID to delete:")
                sql_query = '''
                    DELETE FROM Ingredient
                    WHERE IngredientID = %s;
                '''
                cur_obj.execute(sql_query, (ingredient_id,))
                conn.commit()
                messagebox.showinfo("Info", "Ingredient deleted.")

            def edit_ingredient():
                ingredient_id = simpledialog.askstring("Input", "Enter IngredientID to edit:")
                name = simpledialog.askstring("Input", "Enter new name:")
                description = simpledialog.askstring("Input", "Enter new description:")
                cal = simpledialog.askstring("Input", "Enter new calories:")
                protein = simpledialog.askstring("Input", "Enter new protein:")
                fat = simpledialog.askstring("Input", "Enter new fat:")
                carb = simpledialog.askstring("Input", "Enter new carbs:")
                sql_query = '''
                    UPDATE Ingredient
                    SET name = %s, description = %s, cal = %s, protein = %s, fat = %s, carb = %s
                    WHERE IngredientID = %s;
                '''
                data = (name, description, cal, protein, fat, carb, ingredient_id)
                cur_obj.execute(sql_query, data)
                conn.commit()
                messagebox.showinfo("Info", "Ingredient updated.")

            option = simpledialog.askstring("Input", "Do you want to add, delete, or edit from the ingredients list? (add/delete/edit)")
            if option == "add":
                add_ingredient()
            elif option == "delete":
                delete_ingredient()
            elif option == "edit":
                edit_ingredient()

        def update_recipes():
            def add_recipe():
                name = simpledialog.askstring("Input", "Enter name:")
                instructions = simpledialog.askstring("Input", "Enter instructions:")
                cook_time = simpledialog.askstring("Input", "Enter cook time (minutes):")
                servings = simpledialog.askstring("Input", "Enter servings:")
                category = simpledialog.askstring("Input", "Enter category:")
                sql_query = '''
                    INSERT INTO Recipe (name, instructions, cookTimeMin, servings, category)
                    VALUES (%s, %s, %s, %s, %s);
                '''
                data = (name, instructions, cook_time, servings, category)
                cur_obj.execute(sql_query, data)
                conn.commit()
                messagebox.showinfo("Info", "Recipe added.")

            def delete_recipe():
                recipe_id = simpledialog.askstring("Input", "Enter RecipeID to delete:")
                sql_query = '''
                    DELETE FROM Recipe
                    WHERE RecipeID = %s;
                '''
                cur_obj.execute(sql_query, (recipe_id,))
                conn.commit()
                messagebox.showinfo("Info", "Recipe deleted.")

            def edit_recipe():
                recipe_id = simpledialog.askstring("Input", "Enter RecipeID to edit:")
                name = simpledialog.askstring("Input", "Enter new name:")
                instructions = simpledialog.askstring("Input", "Enter new instructions:")
                cook_time = simpledialog.askstring("Input", "Enter new cook time (minutes):")
                servings = simpledialog.askstring("Input", "Enter new servings:")
                category = simpledialog.askstring("Input", "Enter new category:")
                sql_query = '''
                    UPDATE Recipe
                    SET name = %s, instructions = %s, cookTimeMin = %s, servings = %s, category = %s
                    WHERE RecipeID = %s;
                '''
                data = (name, instructions, cook_time, servings, category, recipe_id)
                cur_obj.execute(sql_query, data)
                conn.commit()
                messagebox.showinfo("Info", "Recipe updated.")

            option = simpledialog.askstring("Input", "Do you want to add, delete, or edit from the recipes list? (add/delete/edit)")
            if option == "add":
                add_recipe()
            elif option == "delete":
                delete_recipe()
            elif option == "edit":
                edit_recipe()

        def update_recipe_ingredients():
            def add_recipe_ingredient():
                recipe_id = simpledialog.askstring("Input", "Enter RecipeID:")
                ingredient_id = simpledialog.askstring("Input", "Enter IngredientID:")
                quantity = simpledialog.askstring("Input", "Enter quantity:")
                unit_measure = simpledialog.askstring("Input", "Enter unit of measure:")
                sql_query = '''
                    INSERT INTO RecipeIngredient (RecipeID, IngredientID, quantity, unitMeasure)
                    VALUES (%s, %s, %s, %s);
                '''
                data = (recipe_id, ingredient_id, quantity, unit_measure)
                cur_obj.execute(sql_query, data)
                conn.commit()
                messagebox.showinfo("Info", "RecipeIngredient added.")

            def delete_recipe_ingredient():
                recipe_ingredient_id = simpledialog.askstring("Input", "Enter RecipeIngredientID to delete:")
                sql_query = '''
                    DELETE FROM RecipeIngredient
                    WHERE RecipeIngredientID = %s;
                '''
                cur_obj.execute(sql_query, (recipe_ingredient_id,))
                conn.commit()
                messagebox.showinfo("Info", "RecipeIngredient deleted.")

            def edit_recipe_ingredient():
                recipe_ingredient_id = simpledialog.askstring("Input", "Enter RecipeIngredientID to edit:")
                recipe_id = simpledialog.askstring("Input", "Enter new RecipeID:")
                ingredient_id = simpledialog.askstring("Input", "Enter new IngredientID:")
                quantity = simpledialog.askstring("Input", "Enter new quantity:")
                unit_measure = simpledialog.askstring("Input", "Enter new unit of measure:")
                sql_query = '''
                    UPDATE RecipeIngredient
                    SET RecipeID = %s, IngredientID = %s, quantity = %s, unitMeasure = %s
                    WHERE RecipeIngredientID = %s;
                '''
                data = (recipe_id, ingredient_id, quantity, unit_measure, recipe_ingredient_id)
                cur_obj.execute(sql_query, data)
                conn.commit()
                messagebox.showinfo("Info", "RecipeIngredient updated.")

            option = simpledialog.askstring("Input", "Do you want to add, delete, or edit from the RecipeIngredient list? (add/delete/edit)")
            if option == "add":
                add_recipe_ingredient()
            elif option == "delete":
                delete_recipe_ingredient()
            elif option == "edit":
                edit_recipe_ingredient()

        window = tk.Toplevel(self.root)
        window.title("Updates")

        frame = ttk.Frame(window, padding="20")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="This page is mostly for backend clean up").grid(column=0, row=0, columnspan=3, pady=10)
        ttk.Button(frame, text="Update Ingredients", command=update_ingredients).grid(column=0, row=1, pady=5, padx=10)
        ttk.Button(frame, text="Update Recipes", command=update_recipes).grid(column=1, row=1, pady=5, padx=10)
        ttk.Button(frame, text="Update RecipeIngredients", command=update_recipe_ingredients).grid(column=2, row=1, pady=5, padx=10)
    #Exports the meal plan to csv
    def export_meal_plan_to_csv(self):
        cur_obj.execute('''
            SELECT * FROM MealPlanView;
        ''')
        meal_plan = cur_obj.fetchall()

        import os
        filename = os.path.join(os.path.dirname(__file__), "..", "resources", "meal_plan_report.csv")
        headers = ["MealPlanID", "MealDate", "RecipeName"]

        try:
            with open(filename, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile)
                csvwriter.writerow(headers)
                csvwriter.writerows(meal_plan)
            messagebox.showinfo("Info", f"Meal plan report successfully exported to {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while exporting the meal plan report: {e}")
    #quit the app and close
    def quit_app(self):
        conn.close()
        self.root.quit()
#main
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
