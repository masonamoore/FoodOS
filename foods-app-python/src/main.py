#import MySQL
import mysql.connector
import csv
import openai
import json

#Make Connection
conn = mysql.connector.connect(host="localhost",
user="root",
password="cpsc408!",
database="Final_Schema",
auth_plugin='mysql_native_password')

#create cursor object
cur_obj = conn.cursor(buffered = True)

#This function handles eveything to do with the meal plan
#It lets you view and edit it and prompts you to do so
def mealPlan():
    print("Made it to Meal plan")
    print()
    print("Do you want to see the meal plan or change it?")
    print("See: 1")
    print("Change: 2")
    choice = input()
    
    if choice == '1':
        # View the meal plan
        cur_obj.execute('''
            SELECT MP.MealPlanID, MP.MealDate, R.name AS RecipeName
            FROM MealPlan MP
            JOIN Recipe R ON MP.RecipeID = R.RecipeID
            ORDER BY MP.MealDate;
        ''')
        meal_plan = cur_obj.fetchall()

        # Print the meal plan
        for item in meal_plan:
            print(item)
    
    elif choice == '2':
        print("Do you want to add a new meal or update an existing one?")
        print("Add: 1")
        print("Update: 2")
        sub_choice = input()
        
        if sub_choice == '1':
            # Add a new meal to the meal plan
            print("Please provide the following details to add a new meal")
            print("Meal Date (YYYY-MM-DD):")
            meal_date = input()
            print("Recipe ID:")
            recipe_id = input()
            
            sql_query = '''
                INSERT INTO MealPlan (MealDate, RecipeID)
                VALUES (%s, %s);
            '''
            data = (meal_date, recipe_id)
            cur_obj.execute(sql_query, data)
            conn.commit()
            print("New meal added to the meal plan.")
        
        elif sub_choice == '2':
            # Update an existing meal in the meal plan
            print("Please provide the following details to update a meal")
            print("Meal Plan ID:")
            meal_plan_id = input()
            print("New Meal Date (YYYY-MM-DD):")
            meal_date = input()
            print("New Recipe ID:")
            recipe_id = input()
            
            sql_query = '''
                UPDATE MealPlan
                SET MealDate = %s, RecipeID = %s
                WHERE MealPlanID = %s;
            '''
            data = (meal_date, recipe_id, meal_plan_id)
            cur_obj.execute(sql_query, data)
            conn.commit()
            print("Meal plan updated.")

#This function handles everything you need with the grocery list
#It lets you add to the list, delete from the list and view your list
def groceryList():
    print("Made it to Grocery List")
    print()
    print("What do you want to do with the Grocery List?")
    print("View: 1")
    print("Add: 2")
    print("Delete: 3")
    choice = input()
    
    if choice == '1':
        cur_obj.execute('''
            SELECT GL.GroceryListID, I.name, GL.store
            FROM GroceryList GL
            JOIN RecipeIngredient RI ON GL.RecipeIngredientID = RI.RecipeIngredientID
            JOIN Ingredient I ON RI.IngredientID = I.IngredientID;
        ''')
        grocery_list = cur_obj.fetchall()

        # Print the grocery list
        for item in grocery_list:
            print(item)
    
    elif choice == '2':
        print("Please provide the following details to add an item to the Grocery List")
        print("Ingredient ID:")
        ingredient_id = input()
        print("Store:")
        store = input()
        
        # Find the corresponding RecipeIngredientID
        cur_obj.execute('''
            SELECT RecipeIngredientID
            FROM RecipeIngredient
            WHERE IngredientID = %s;
        ''', (ingredient_id,))
        recipe_ingredient_id = cur_obj.fetchone()

        # Ensure the result is fetched before executing another query
        if recipe_ingredient_id:
            sql_query = '''
                INSERT INTO GroceryList (RecipeIngredientID, store)
                VALUES (%s, %s);
            '''
            data = (recipe_ingredient_id[0], store)
            cur_obj.execute(sql_query, data)
            conn.commit()
            print("Item added to the Grocery List.")
        else:
            print("No matching RecipeIngredient found for the provided Ingredient ID.")
    
    elif choice == '3':
        print("Please provide the Grocery List ID of the item you want to delete:")
        grocery_list_id = input()
        sql_query = '''
            DELETE FROM GroceryList
            WHERE GroceryListID = %s;
        '''
        cur_obj.execute(sql_query, (grocery_list_id,))
        conn.commit()
        print("Item deleted from the Grocery List.")



#This function has the most queries
#It allows you to sort though your recipes in any way you'd like
#All of the different options are presented to you in the print statements below
def recipes():
    print("Made it to recipes")
    print()
    print("How do you want to see the recipes sorted?")
    print("Alphabetical: 1")
    print("By meal type (Breakfast, lunch...): 2")
    print()
    print("Cooking time quick: 3")
    print("Cooking time medium: 4")
    print("Cooking time long: 5")
    print()
    print("Do you want to see recipes you can make with the ingredients you have?: 6")
    print("Do you want to see recipes where you are only missing a few ingredients?: 7")
    print("Do you want to see recipes that are on this week's meal plan and you have the ingredients?: 8")
    print()
    print("Low Calorie: 9")
    print("Medium Calorie: 10")
    print("High Calorie: 11")
    choice = input()
    if choice == '1':
        cur_obj.execute("SELECT name, instructions FROM Recipe ORDER BY name;")
        recipes = cur_obj.fetchall()

        # Print the sorted recipes
        for recipe in recipes:
            print(recipe)
    elif choice == '2':
        print("Specify the meal type (Breakfast, Lunch, Dinner, Snack):")
        meal_type = input()
        cur_obj.execute("SELECT name, instructions FROM Recipe WHERE category = %s ORDER BY name;", (meal_type,))
        recipes = cur_obj.fetchall()

        # Print the sorted recipes
        for recipe in recipes:
            print(recipe)
    elif choice == '3':
        cur_obj.execute("SELECT name, instructions, cookTimeMin FROM Recipe WHERE cookTimeMin <= 15;")
        recipes = cur_obj.fetchall()

        # Print the sorted recipes
        for recipe in recipes:
            print(recipe)
    elif choice == '4':
        cur_obj.execute("SELECT name, instructions, cookTimeMin FROM Recipe WHERE cookTimeMin > 15 AND cookTimeMin <= 45;")
        recipes = cur_obj.fetchall()

        # Print the sorted recipes
        for recipe in recipes:
            print(recipe)
    elif choice == '5':
        cur_obj.execute("SELECT name, instructions, cookTimeMin FROM Recipe WHERE cookTimeMin > 45;")
        recipes = cur_obj.fetchall()

        # Print the sorted recipes
        for recipe in recipes:
            print(recipe)
    elif choice == '6':
        cur_obj.execute('''
            SELECT DISTINCT R.name
            FROM Recipe R
            JOIN RecipeIngredient RI ON R.RecipeID = RI.RecipeID
            JOIN Inventory I ON RI.IngredientID = I.IngredientID
            WHERE I.quantity > 0;
        ''')
        recipes = cur_obj.fetchall()

        # Print the sorted recipes
        for recipe in recipes:
            print(recipe)
    elif choice == '7':
        print("Specify the maximum number of missing ingredients:")
        max_missing = input()
        cur_obj.execute('''
            SELECT R.name
            FROM Recipe R
            JOIN RecipeIngredient RI ON R.RecipeID = RI.RecipeID
            LEFT JOIN Inventory I ON RI.IngredientID = I.IngredientID AND I.quantity > 0
            GROUP BY R.RecipeID, R.name
            HAVING COUNT(CASE WHEN I.IngredientID IS NULL THEN 1 END) <= %s;
        ''', (max_missing,))
        recipes = cur_obj.fetchall()

        # Print the sorted recipes
        for recipe in recipes:
            print(recipe)
    elif choice == '8':
        cur_obj.execute('''
            SELECT R.name
            FROM MealPlan MP
            JOIN Recipe R ON MP.RecipeID = R.RecipeID
            JOIN RecipeIngredient RI ON R.RecipeID = RI.RecipeID
            JOIN Inventory I ON RI.IngredientID = I.IngredientID
            WHERE I.quantity > 0
            GROUP BY R.RecipeID, R.name
            HAVING COUNT(DISTINCT RI.IngredientID) = COUNT(DISTINCT I.IngredientID);
        ''')
        recipes = cur_obj.fetchall()

        # Print the sorted recipes
        for recipe in recipes:
            print(recipe)
    elif choice == '9':
        cur_obj.execute('''
            SELECT R.name, R.instructions
            FROM Recipe R
            JOIN RecipeIngredient RI ON R.RecipeID = RI.RecipeID
            JOIN Ingredient I ON RI.IngredientID = I.IngredientID
            GROUP BY R.name, R.instructions
            HAVING SUM(I.cal * RI.quantity) <= 300;
        ''')
        recipes = cur_obj.fetchall()

        # Print the sorted recipes
        for recipe in recipes:
            print(recipe)
    elif choice == '10':
        cur_obj.execute('''
            SELECT R.name, R.instructions
            FROM Recipe R
            JOIN RecipeIngredient RI ON R.RecipeID = RI.RecipeID
            JOIN Ingredient I ON RI.IngredientID = I.IngredientID
            GROUP BY R.name, R.instructions
            HAVING SUM(I.cal * RI.quantity) > 300 AND SUM(I.cal * RI.quantity) <= 600;
        ''')
        recipes = cur_obj.fetchall()

        # Print the sorted recipes
        for recipe in recipes:
            print(recipe)
    elif choice == '11':
        cur_obj.execute('''
            SELECT R.name, R.instructions
            FROM Recipe R
            JOIN RecipeIngredient RI ON R.RecipeID = RI.RecipeID
            JOIN Ingredient I ON RI.IngredientID = I.IngredientID
            GROUP BY R.name, R.instructions
            HAVING SUM(I.cal * RI.quantity) > 600;
        ''')
        recipes = cur_obj.fetchall()

        # Print the sorted recipes
        for recipe in recipes:
            print(recipe)


#This is the inventory function that allows for you to view and edit your inventory
#you can add to it and also view what ingredients you have in your house 
#even lets you sort by where the items are in your house
def inventory():
    print("Made it to inventory")
    print("Display all my ingredients: 1")
    print("Display ingredients in my fridge: 2")
    print("Display ingredients in my freezer: 3")
    print("Display ingredients in my pantry: 4")
    print("Change inventory status: 5")
    choice = input()
    if choice == '1':
        cur_obj.execute("""
            SELECT ing.name 
            FROM Inventory inv
            JOIN Ingredient ing ON inv.IngredientID = ing.IngredientID
            WHERE inv.quantity > 0;
        """)
        ingredients = cur_obj.fetchall()

        # Print the ingredients
        for ingredient in ingredients:
            print(ingredient)
    
    elif choice == '2':
        cur_obj.execute("""
            SELECT ing.name 
            FROM Inventory inv
            JOIN Ingredient ing ON inv.IngredientID = ing.IngredientID
            WHERE inv.quantity > 0 AND inv.location = 'fridge';
        """)
        fridge_ingredients = cur_obj.fetchall()

        # Print the ingredients in the fridge
        for ingredient in fridge_ingredients:
            print(ingredient)

    elif choice == '3':
        cur_obj.execute("""
            SELECT ing.name 
            FROM Inventory inv
            JOIN Ingredient ing ON inv.IngredientID = ing.IngredientID
            WHERE inv.quantity > 0 AND inv.location = 'freezer';
        """)
        freezer_ingredients = cur_obj.fetchall()

        # Print the ingredients in the freezer
        for ingredient in freezer_ingredients:
            print(ingredient)

    elif choice == '4':
        cur_obj.execute("""
            SELECT ing.name 
            FROM Inventory inv
            JOIN Ingredient ing ON inv.IngredientID = ing.IngredientID
            WHERE inv.quantity > 0 AND inv.location = 'pantry';
        """)
        pantry_ingredients = cur_obj.fetchall()

        # Print the ingredients in the pantry
        for ingredient in pantry_ingredients:
            print(ingredient)

    elif choice == '5':
        print("Please tell me the ingredient ID")
        ingredientID = input()
        print("Now tell me the new quantity")
        quantity = input()
        sql_query = "UPDATE Inventory SET quantity = %s WHERE IngredientID = %s;"
        data = (quantity, ingredientID)
        cur_obj.execute(sql_query, data)
        conn.commit()


#This function handles all of the updates you may need
#It lets you update all the different aspects of your tables and do the backend work you may need to do
#It lets you edit things like Final_Schema.RecipeIngredient which holds the foriegn keys to connect 
#Recipes and ingredients
def updates():
    print("Made it to updates")
    print("This page is mostly for backend clean up")
    print()
    print("Update ingredients: 1")
    print("Update recipes: 2")
    print("Update RecipeIngredient (This is the list of what ingredients are in which recipes): 3")
    choice = input()
    
    if choice == '1':
        print()
        print("Do you want to add, delete, or edit from the ingredients list?")
        print("Add: 1")
        print("Delete: 2")
        print("Edit: 3")
        choice2 = input()
        
        if choice2 == '1':
            print("Enter name: ")
            name = input()
            print("Enter description: ")
            description = input()
            print("Enter calories: ")
            cal = input()
            print("Enter protein: ")
            protein = input()
            print("Enter fat: ")
            fat = input()
            print("Enter carbs: ")
            carb = input()
            
            sql_query = '''
                INSERT INTO Ingredient (name, description, cal, protein, fat, carb)
                VALUES (%s, %s, %s, %s, %s, %s);
            '''
            data = (name, description, cal, protein, fat, carb)
            cur_obj.execute(sql_query, data)
            conn.commit()
            print("Ingredient added.")
        
        elif choice2 == '2':
            print("Enter IngredientID to delete: ")
            IngredientID = input()
            
            sql_query = '''
                DELETE FROM Ingredient
                WHERE IngredientID = %s;
            '''
            cur_obj.execute(sql_query, (IngredientID,))
            conn.commit()
            print("Ingredient deleted.")
        
        elif choice2 == '3':
            print("Enter IngredientID to edit: ")
            IngredientID = input()
            print("Enter new name: ")
            name = input()
            print("Enter new description: ")
            description = input()
            print("Enter new calories: ")
            cal = input()
            print("Enter new protein: ")
            protein = input()
            print("Enter new fat: ")
            fat = input()
            print("Enter new carbs: ")
            carb = input()
            
            sql_query = '''
                UPDATE Ingredient
                SET name = %s, description = %s, cal = %s, protein = %s, fat = %s, carb = %s
                WHERE IngredientID = %s;
            '''
            data = (name, description, cal, protein, fat, carb, IngredientID)
            cur_obj.execute(sql_query, data)
            conn.commit()
            print("Ingredient updated.")
    
    elif choice == '2':
        print()
        print("Do you want to add, delete, or edit from the recipes list?")
        print("Add: 1")
        print("Delete: 2")
        print("Edit: 3")
        choice2 = input()
        
        if choice2 == '1':
            print("Enter name: ")
            name = input()
            print("Enter instructions: ")
            instructions = input()
            print("Enter cook time (minutes): ")
            cookTimeMin = input()
            print("Enter servings: ")
            servings = input()
            print("Enter category: ")
            category = input()
            
            sql_query = '''
                INSERT INTO Recipe (name, instructions, cookTimeMin, servings, category)
                VALUES (%s, %s, %s, %s, %s);
            '''
            data = (name, instructions, cookTimeMin, servings, category)
            cur_obj.execute(sql_query, data)
            conn.commit()
            print("Recipe added.")
        
        elif choice2 == '2':
            print("Enter RecipeID to delete: ")
            RecipeID = input()
            
            sql_query = '''
                DELETE FROM Recipe
                WHERE RecipeID = %s;
            '''
            cur_obj.execute(sql_query, (RecipeID,))
            conn.commit()
            print("Recipe deleted.")
        
        elif choice2 == '3':
            print("Enter RecipeID to edit: ")
            RecipeID = input()
            print("Enter new name: ")
            name = input()
            print("Enter new instructions: ")
            instructions = input()
            print("Enter new cook time (minutes): ")
            cookTimeMin = input()
            print("Enter new servings: ")
            servings = input()
            print("Enter new category: ")
            category = input()
            
            sql_query = '''
                UPDATE Recipe
                SET name = %s, instructions = %s, cookTimeMin = %s, servings = %s, category = %s
                WHERE RecipeID = %s;
            '''
            data = (name, instructions, cookTimeMin, servings, category, RecipeID)
            cur_obj.execute(sql_query, data)
            conn.commit()
            print("Recipe updated.")
    
    elif choice == '3':
        print()
        print("Do you want to add, delete, or edit from the RecipeIngredient list?")
        print("Add: 1")
        print("Delete: 2")
        print("Edit: 3")
        choice2 = input()
        
        if choice2 == '1':
            print("Enter RecipeID: ")
            RecipeID = input()
            print("Enter IngredientID: ")
            IngredientID = input()
            print("Enter quantity: ")
            quantity = input()
            print("Enter unit of measure: ")
            unitMeasure = input()
            
            sql_query = '''
                INSERT INTO RecipeIngredient (RecipeID, IngredientID, quantity, unitMeasure)
                VALUES (%s, %s, %s, %s);
            '''
            data = (RecipeID, IngredientID, quantity, unitMeasure)
            cur_obj.execute(sql_query, data)
            conn.commit()
            print("RecipeIngredient added.")
        
        elif choice2 == '2':
            print("Enter RecipeIngredientID to delete: ")
            RecipeIngredientID = input()
            
            sql_query = '''
                DELETE FROM RecipeIngredient
                WHERE RecipeIngredientID = %s;
            '''
            cur_obj.execute(sql_query, (RecipeIngredientID,))
            conn.commit()
            print("RecipeIngredient deleted.")
        
        elif choice2 == '3':
            print("Enter RecipeIngredientID to edit: ")
            RecipeIngredientID = input()
            print("Enter new RecipeID: ")
            RecipeID = input()
            print("Enter new IngredientID: ")
            IngredientID = input()
            print("Enter new quantity: ")
            quantity = input()
            print("Enter new unit of measure: ")
            unitMeasure = input()
            
            sql_query = '''
                UPDATE RecipeIngredient
                SET RecipeID = %s, IngredientID = %s, quantity = %s, unitMeasure = %s
                WHERE RecipeIngredientID = %s;
            '''
            data = (RecipeID, IngredientID, quantity, unitMeasure, RecipeIngredientID)
            cur_obj.execute(sql_query, data)
            conn.commit()
            print("RecipeIngredient updated.")

#This function reads from a view I created in the schema
#It then creates a .csv file where it creates a nice read
#of your meal plans. The meal plans have the recipe and the date 
def export_meal_plan_to_csv():
    print("Exporting meal plan to CSV...")
    cur_obj.execute('''
        SELECT * FROM MealPlanView;
    ''')
    meal_plan = cur_obj.fetchall()

    # Specify the file name
    import os
    filename = os.path.join(os.path.dirname(__file__), "..", "resources", "meal_plan_report.csv")

    # Column headers
    headers = ["MealPlanID", "MealDate", "RecipeName"]

    try:
        # Open the file in write mode
        with open(filename, 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(headers)
            csvwriter.writerows(meal_plan)

        print(f"Meal plan report successfully exported to {filename}")
    except Exception as e:
        print(f"An error occurred while exporting the meal plan report: {e}")

#Start of New AI code
def generate_ai_recipe():
    print("What kind of recipe would you like? (e.g., 'vegan taco under 20 minutes')")
    prompt = input("Enter prompt: ")

    print("Generating recipe using AI...")

    client = openai.OpenAI(api_key="ADD_YOUR_API_KEY_HERE")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful chef assistant. Respond ONLY in JSON format."},
            {"role": "user", "content": f"""
Please generate a recipe based on this: {prompt}

Respond in this exact JSON format:
{{
  "name": "Recipe Name",
  "instructions": "Step-by-step cooking instructions.",
  "cookTimeMin": 20,
  "servings": 2,
  "category": "Lunch",
  "ingredients": [
    {{
      "name": "Ingredient 1",
      "quantity": 1,
      "unit": "cup"
    }},
    {{
      "name": "Ingredient 2",
      "quantity": 2,
      "unit": "tablespoons"
    }}
  ]
}}
"""}
        ]
    )

    try:
        recipe_json = json.loads(response.choices[0].message.content)
    except json.JSONDecodeError:
        print("❌ Failed to parse the AI response. Try again.")
        return

    print("\n✅ Recipe Preview:")
    print("Name:", recipe_json["name"])
    print("Servings:", recipe_json["servings"])
    print("Cook Time (min):", recipe_json["cookTimeMin"])
    print("Category:", recipe_json["category"])
    print("Ingredients:")
    for ing in recipe_json["ingredients"]:
        print(f"  - {ing['quantity']} {ing['unit']} {ing['name']}")
    print("Instructions:")
    print(recipe_json["instructions"][:200] + "...")

    print("\nWould you like to save this recipe to the database? (y/n)")
    if input().lower() != 'y':
        return

    # ✅ Manually assign a new RecipeID
    cur_obj.execute("SELECT MAX(RecipeID) FROM Recipe")
    max_id = cur_obj.fetchone()[0] or 0
    next_id = max_id + 1

    # Insert Recipe with explicit RecipeID
    cur_obj.execute('''
        INSERT INTO Recipe (RecipeID, name, instructions, cookTimeMin, servings, category)
        VALUES (%s, %s, %s, %s, %s, %s)
    ''', (
        next_id,
        recipe_json["name"],
        recipe_json["instructions"],
        recipe_json["cookTimeMin"],
        recipe_json["servings"],
        recipe_json["category"]
    ))
    conn.commit()

    # Use next_id as RecipeID for related RecipeIngredient inserts
    for ing in recipe_json["ingredients"]:
        # Check if ingredient already exists
        cur_obj.execute("SELECT IngredientID FROM Ingredient WHERE name = %s", (ing["name"],))
        row = cur_obj.fetchone()

        if row:
            ingredient_id = row[0]
        else:
            # Insert new ingredient
            cur_obj.execute("INSERT INTO Ingredient (name, description, cal, protein, fat, carb) VALUES (%s, '', 0, 0, 0, 0)", (ing["name"],))
            conn.commit()
            cur_obj.execute("SELECT LAST_INSERT_ID()")
            ingredient_id = cur_obj.fetchone()[0]

        # Get next available RecipeIngredientID
        cur_obj.execute("SELECT MAX(RecipeIngredientID) FROM RecipeIngredient")
        max_ri_id = cur_obj.fetchone()[0] or 0
        next_ri_id = max_ri_id + 1

        # Insert into RecipeIngredient with explicit ID
        cur_obj.execute('''
            INSERT INTO RecipeIngredient (RecipeIngredientID, RecipeID, IngredientID, quantity, unitMeasure)
            VALUES (%s, %s, %s, %s, %s)
        ''', (next_ri_id, next_id, ingredient_id, ing["quantity"], ing["unit"]))
        conn.commit()

    print("🎉 Recipe and ingredients added to the database!")

        
#END of new AI code

# Main function to run the program
def main():

    #Welcomes you to the foods app and then prompts you of all of the different 
    #options you have to edit and view the app
    print("Welcome to Foods!")
    while True:
        print("Please select an option:")
        print("Meal plan: 1")
        print("Grocery List: 2")
        print("Recipes: 3")
        print("Inventory: 4")
        print("Updates: 5")
        print("QUIT: 6")
        print("Export Meal Plan: 7")
        print("Ask AI: 8")
        choice = input()
        if choice == '1':
            mealPlan()
        elif choice == '2':
            groceryList()
        elif choice == '3':
            recipes()
        elif choice == '4':
            inventory()
        elif choice == '5':
            updates()
        elif choice == '6':
            quit()
        elif choice == '7':
            export_meal_plan_to_csv()
        elif choice == '8':
            generate_ai_recipe()
        else:
            print("Invalid input. Please enter a valid response")



if __name__ == "__main__":
    print(conn)
    main()
    conn.close()
    print("closed")