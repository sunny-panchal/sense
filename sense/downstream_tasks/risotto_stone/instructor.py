"""
Cooking instructor to navigate users through a recipe.
"""
import os
import time
import yaml

import numpy as np
from typing import Dict

from sense import SOURCE_DIR
from sense.display import BaseDisplay
from sense.display import put_text
from sense.downstream_tasks.risotto_stone import ENABLED_LABELS
from sense.downstream_tasks.risotto_stone import LAB_THRESHOLDS

ADDING_INGREDIENT = 'adding_ingredient_tag_1'
CHOPPING = 'chopping_tag_1'
PLACING_POT = 'placing_pot_tag_1'
READY = 'ready_tag_1'
STIRRING = 'stirring_pot_tag_1'
TASTING = 'tasting_tag_1'


class RecipeInstructor(BaseDisplay):
    recipes_path = os.path.join(SOURCE_DIR, "downstream_tasks", "risotto_stone", "recipes.yaml")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # initialize state of the recipe
        self.instruction_idx = 0
        self.instruction = ''
        self.play_instruction = False
        self.instruction_lock = False  # block further updates until current instruction is done
        self.unlock_conditions = {}
        self.old_event_counts = {label: 0 for label in ENABLED_LABELS}

        self.monitor = {}  # Any actions that need to be monitored for continued activity

        # load the recipe
        with open(self.recipes_path, 'r') as f:
            self.recipe = yaml.load(f)['CreamyMushroomRisotto']
        self.ingredients = self.recipe["ingredients"]
        self.ingredients_to_prep = [ingredient for ingredient in self.ingredients
                                    if self.ingredients[ingredient].get('prep')]
        self.instructions = self.recipe["instructions"]

    def instruct_ingredient_prep(self, ingredient):
        self.instruction = f"{self.ingredients[ingredient]['prep'].capitalize()} the {ingredient}"
        self.play_instruction = True
        self.instruction_lock = True
        self.ingredients_to_prep.pop(0)
        self.unlock_conditions = {
            READY: LAB_THRESHOLDS[READY]
        }

    def give_next_instruction(self):
        instruction_spec = self.instructions[self.instruction_idx]
        self.instruction = instruction_spec['instruction']
        self.play_instruction = True
        self.instruction_lock = True
        self.unlock_conditions = {
            exit_condition: LAB_THRESHOLDS[exit_condition]
            for exit_condition in instruction_spec['exit_conditions']
        }

        if instruction_spec.get('monitor'):
            self.monitor = instruction_spec['monitor']

    def check_instruction_done(self, event_counts):
        conditions_met = [event_counts[condition] > self.old_event_counts[condition]
                          for condition in self.unlock_conditions]

        if any(conditions_met):
            self.instruction = ''
            self.instruction_lock = False
            self.unlock_conditions = {}
            self.monitor = {}

            if not self.ingredients_to_prep:
                self.instruction_idx += 1

        self.old_event_counts = event_counts

    def check_monitor_conditions(self, predictions):
        now = time.time()
        for label in self.monitor:
            if predictions[label] > LAB_THRESHOLDS[label] or not self.monitor[label].get('time_last_active'):
                self.monitor[label]['time_last_active'] = now
                self.instruction = self.instructions[self.instruction_idx]['instruction']
            elif (now - self.monitor[label]['time_last_active']) > self.monitor[label]['warn_after']:
                if self.instruction is not self.monitor[label]['message']:
                    self.instruction = self.monitor[label]['message']
                    self.play_instruction = True

                    # Play an alert tone
                    for i in range(3):
                        os.system("play -q -n synth 0.15 sin 880")

    def update_instructor(self, display_data):
        event_counts = {k: v for k, v in display_data['counting'].items()}
        predictions = {k: v for k, v in display_data['sorted_predictions']}
        if not self.instruction_lock:
            if self.ingredients_to_prep:
                self.instruct_ingredient_prep(self.ingredients_to_prep[0])
            else:
                self.give_next_instruction()
        else:
            self.check_instruction_done(event_counts)

        # TODO: Clean
        if self.instruction and self.monitor:
            self.check_monitor_conditions(predictions)

    def display(self, img: np.ndarray, display_data: Dict) -> np.ndarray:
        self.update_instructor(display_data)

        if self.play_instruction and self.instruction:
            os.system(f"spd-say -t female2 '{self.instruction}'")
            self.play_instruction = False

        return put_text(img, self.instruction, (5, 70), font_scale=1.2,
                        thickness=1, color=(255, 255, 255))
