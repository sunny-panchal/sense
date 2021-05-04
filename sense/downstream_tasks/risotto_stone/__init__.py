# with background
LAB2INT = {
  "adding_ingredient_tag_1": 0,
  "adding_ingredient_tag_2": 1,
  "background": 2,
  "background_tag_1": 3,
  "background_tag_2": 4,
  "chopping_tag_1": 5,
  "chopping_tag_2": 6,
  "placing_pot_tag_1": 7,
  "placing_pot_tag_2": 8,
  "ready_tag_1": 9,
  "ready_tag_2": 10,
  "stirring_pot_tag_1": 11,
  "stirring_pot_tag_2": 12,
  "tasting_tag_1": 13,
  "tasting_tag_2": 14
}

# without background
# LAB2INT = {
#   "adding_ingredient_tag_1": 0,
#   "adding_ingredient_tag_2": 1,
#   "background": 2,
#   "chopping_tag_1": 3,
#   "chopping_tag_2": 4,
#   "placing_pot_tag_1": 5,
#   "placing_pot_tag_2": 6,
#   "ready_tag_1": 7,
#   "ready_tag_2": 8,
#   "stirring_pot_tag_1": 9,
#   "stirring_pot_tag_2": 10,
#   "tasting_tag_1": 11,
#   "tasting_tag_2": 12
# }

INT2LAB = {v: k for k, v in LAB2INT.items()}

ENABLED_LABELS = [
    "adding_ingredient_tag_1",
    "background",
    "chopping_tag_1",
    "placing_pot_tag_1",
    "ready_tag_1",
    "stirring_pot_tag_1",
    "tasting_tag_1",
]

LAB_THRESHOLDS = {key: 0.7 if key in ENABLED_LABELS else 1. for key in LAB2INT}
LAB_THRESHOLDS["ready_tag_1"] = 0.9
LAB_THRESHOLDS["stirring_pot_tag_1"] = 0.4
