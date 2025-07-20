from backend.steps import TextStep, ImageStep

class DynamicContentLoader:
    def __init__(self, recipe):
        self.recipe = recipe
        # Stores the recipe object locally so that the step attributes can be accessed.
        self.step_objects = []
        # Initialises an empty list to hold the step objects.

        for s in recipe.steps:
            # Loops over steps stored in recipe to determine if they're text only or include images.
            if s.img_path:
                self.step_objects.append(ImageStep(s.step_number, s.instruction, s.img_path))
                # Renders step with image if the step includes an img_path.
            else:
                self.step_objects.append(TextStep(s.step_number, s.instruction))
                # Renders only the step number and instruction if no img_path is included.

    def get_rendered_steps(self) -> list[str]:
        return [step.render() for step in self.step_objects]
        # Generated and returns a list of rendered HTML strings for each step.
        # Each step object will implement it's own render method (an example of polymorphism)
#
# Aggregates different types of steps into one list: self.step_objects
# This way the steps can be looped over and rendered as a group.