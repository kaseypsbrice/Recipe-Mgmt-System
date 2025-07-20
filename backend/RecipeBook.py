class RecipeBook:
    def __init__(self, source=None):
        if source is None:
            self.recipes = []
            # Creates an empty recipe book
        else:
            self.recipes = source
            # Loads from an existing list or file

    def add_recipe(self, recipe):
        self.recipes.append(recipe)

    def log_full_recipes(self, user, file_path="backend/static/saved_recipes/saved_recipes.txt"):
        with open(file_path, "a") as f:
            for recipe in self.recipes:
                f.write("\n")
                f.write(f"Recipe ID: {recipe.recipe_id}\n")
                f.write(f"Name: {recipe.name}\n")
                f.write(f"Description: {recipe.description}\n")
                f.write(f"Servings: {recipe.servings}\n")
                f.write(f"Cook Time: {recipe.cook_time_min} min\n")
                f.write(f"Created by: {user.username}\n")

                f.write("Ingredients:\n")
                for ing in recipe.ingredients:
                    f.write(f"  • {ing.quantity} {ing.unit} {ing.name}\n")

                f.write("Steps:\n")
                for s in recipe.steps:
                    f.write(f"  {s.step_number}. {s.instruction}\n")
                    if s.img_path:
                        f.write(f"Image: {s.img_path}\n")

                f.write("-" * 40 + "\n")
    # Logs all recipes in RecipeBook to a text file.
    
    def load_recipes_from_file(file_path="backend/static/saved_recipes/saved_recipes.txt") -> list:
        recipes = []
        try:
            with open(file_path, "r") as f:
                lines = [line.strip() for line in f.readlines()]
        except FileNotFoundError:
            return []

        current_recipe = {}
        current_ingredients = []
        current_steps = []

        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith("Recipe ID:"):
                current_recipe = {
                    "recipe_id": int(line.split(":")[1].strip())
                }
                current_ingredients = []
                current_steps = []
            elif line.startswith("Name:"):
                current_recipe["name"] = line.split(":", 1)[1].strip()
            elif line.startswith("Description:"):
                current_recipe["description"] = line.split(":", 1)[1].strip()
            elif line.startswith("Servings:"):
                current_recipe["servings"] = int(line.split(":", 1)[1].strip())
            elif line.startswith("Cook Time:"):
                current_recipe["cook_time_min"] = int(line.split()[2])
            elif line.startswith("Ingredients:"):
                i += 1
                while i < len(lines) and lines[i].startswith("•"):
                    parts = lines[i][2:].split(" ")
                    quantity = float(parts[0])
                    unit = parts[1]
                    name = " ".join(parts[2:])
                    current_ingredients.append({
                        "name": name,
                        "quantity": quantity,
                        "unit": unit
                    })
                    i += 1
                i -= 1  # rewind so main loop doesn't skip a line
            elif line.startswith("Steps:"):
                i += 1
                while i < len(lines) and lines[i] and not lines[i].startswith("-"):
                    if ". " in lines[i]:
                        step_number, instruction = lines[i].split(". ", 1)
                        img_path = None
                        if i+1 < len(lines) and lines[i+1].startswith("📷"):
                            img_path = lines[i+1].split(": ", 1)[1].strip()
                            i += 1
                        current_steps.append({
                            "step_number": int(step_number),
                            "instruction": instruction,
                            "img_path": img_path
                        })
                    i += 1
            elif line.startswith("-" * 10):
                # end of a recipe block
                current_recipe["ingredients"] = current_ingredients
                current_recipe["steps"] = current_steps
                recipes.append(current_recipe)
            i += 1

        return recipes