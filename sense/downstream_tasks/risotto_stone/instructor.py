"""
Cooking instructor to navigate users through a recipe.
"""
import os
import yaml

import numpy as np
from typing import Dict

from sense import SOURCE_DIR
from sense.display import BaseDisplay
from sense.display import put_text

ADDING_INGREDIENT = 'adding_ingredient_tag_1'
CHOPPING = 'chopping_tag_1'
PLACING_POT = 'placing_pot_tag_1'
READY = 'ready_tag_1'
STIRRING = 'stirring_pot_tag_1'
TASTING = 'tasting_tag_1'

THRESHOLDS = {
    ADDING_INGREDIENT: 0.5,
    CHOPPING: 0.5,
    PLACING_POT: 0.5,
    READY: 0.9,
    STIRRING: 0.5,
    TASTING: 0.5,
}


class RecipeInstructor(BaseDisplay):
    recipes_path = os.path.join(SOURCE_DIR, "downstream_tasks", "risotto_stone", "recipes.yaml")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # initialize state of the recipe
        self.instruction_idx = 0
        self.instruction = ''
        self.instruction_lock = False  # block further updates until current instruction is done
        self.unlock_conditions = {}

        # load the recipe
        with open(self.recipes_path, 'r') as f:
            self.recipe = yaml.load(f)['CreamyMushroomRisotto']
        self.ingredients = self.recipe["ingredients"]
        self.ingredients_to_prep = [ingredient for ingredient in self.ingredients
                                    if self.ingredients[ingredient].get('prep')]
        self.instructions = self.recipe["instructions"]

    def instruct_ingredient_prep(self, ingredient):
        self.instruction = f"Prepare the {ingredient} ({self.ingredients[ingredient]['prep']})"
        self.instruction_lock = True
        self.ingredients_to_prep.pop(0)
        self.unlock_conditions = {
            READY: THRESHOLDS[READY]
        }

    def give_next_instruction(self):
        instruction_spec = self.instructions[self.instruction_idx]
        self.instruction = instruction_spec['instruction']
        self.instruction_lock = True
        self.unlock_conditions = {
            exit_condition: THRESHOLDS[exit_condition]
            for exit_condition in instruction_spec['exit_conditions']
        }

    # TODO: this should check if action is complete? Returned to background?
    def check_instruction_done(self, predictions):
        conditions_met = [predictions[condition] > self.unlock_conditions[condition]
                          for condition in self.unlock_conditions]

        if any(conditions_met):
            self.instruction = ''
            self.instruction_lock = False
            self.unlock_conditions = {}  # REVIEW: Reset needed?

            if not self.ingredients_to_prep:
                self.instruction_idx += 1

    def update_instructor(self, predictions):
        if not self.instruction_lock:
            if self.ingredients_to_prep:
                self.instruct_ingredient_prep(self.ingredients_to_prep[0])
            else:
                self.give_next_instruction()
        else:
            self.check_instruction_done(predictions)

    def display(self, img: np.ndarray, display_data: Dict) -> np.ndarray:
        predictions = {k: v for k, v in display_data['sorted_predictions']}

        self.update_instructor(predictions)

        return put_text(img, self.instruction, (5, 70), font_scale=2,
                        thickness=2, color=(255, 255, 255))


# TODO:
#   - Smooth predictions
#   - Gate predictions with background
#   - Add cooldown to actions