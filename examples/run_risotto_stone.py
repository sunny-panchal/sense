#!/usr/bin/env python
"""
Cooking assistant to help you make the perfect risotto.

Basic cooking actions detected are:
    - adding an ingredient to a pot
    - stirring the pot
    - placing the pot
    - tasting the food
    - chopping ingredients
    - thumbs up to signal being ready

Usage:
  run_risotto_stone.py  [--camera_id=CAMERA_ID]
                        [--path_in=FILENAME]
                        [--path_out=FILENAME]
                        [--title=TITLE]
                        [--use_gpu]
  run_risotto_stone.py (-h | --help)

Options:
  --camera_id=CAMERA_ID           ID of the camera to stream from
  --path_in=FILENAME              Video file to stream from
  --path_out=FILENAME             Video file to stream to
  --title=TITLE                   This adds a title to the window display
  --use_gpu                       Whether to run inference on the GPU or not.
"""
from docopt import docopt

import sense.display
from sense.controller import Controller
from sense.downstream_tasks.nn_utils import Pipe
from sense.downstream_tasks.nn_utils import LogisticRegression
from sense.downstream_tasks.postprocess import PostprocessClassificationOutput
from sense.loading import build_backbone_network
from sense.loading import load_weights_from_resources
from sense.loading import update_backbone_weights
from sense.loading import ModelConfig


# with background
# LAB2INT = {
#   "adding_ingredient_tag_1": 0,
#   "adding_ingredient_tag_2": 1,
#   "background": 2,
#   "background_tag_1": 3,
#   "background_tag_2": 4,
#   "chopping_tag_1": 5,
#   "chopping_tag_2": 6,
#   "placing_pot_tag_1": 7,
#   "placing_pot_tag_2": 8,
#   "ready_tag_1": 9,
#   "ready_tag_2": 10,
#   "stirring_pot_tag_1": 11,
#   "stirring_pot_tag_2": 12,
#   "tasting_tag_1": 13,
#   "tasting_tag_2": 14
# }

# without background
LAB2INT = {
  "adding_ingredient_tag_1": 0,
  "adding_ingredient_tag_2": 1,
  "background": 2,
  "chopping_tag_1": 3,
  "chopping_tag_2": 4,
  "placing_pot_tag_1": 5,
  "placing_pot_tag_2": 6,
  "ready_tag_1": 7,
  "ready_tag_2": 8,
  "stirring_pot_tag_1": 9,
  "stirring_pot_tag_2": 10,
  "tasting_tag_1": 11,
  "tasting_tag_2": 12
}

INT2LAB = {v: k for k, v in LAB2INT.items()}


if __name__ == "__main__":
    # Parse arguments
    args = docopt(__doc__)
    use_gpu = args['--use_gpu']
    camera_id = int(args['--camera_id'] or 0)
    path_in = args['--path_in'] or None
    path_out = args['--path_out'] or None
    title = args['--title'] or None

    # Load backbone network according to config file
    backbone_model_config = ModelConfig('StridedInflatedEfficientNet', 'pro', [])
    backbone_weights = backbone_model_config.load_weights()['backbone']

    # Load custom classifier
    # checkpoint_classifier = load_weights_from_resources('risotto_stone/sien_pro_risotto_stone_no_bg.ckpt')
    checkpoint_classifier = load_weights_from_resources('risotto_stone/sien_pro_risotto_stone_no_bg_16.ckpt')
    # checkpoint_classifier = load_weights_from_resources('risotto_stone/sien_pro_risotto_stone_bg.ckpt')
    # checkpoint_classifier = load_weights_from_resources('risotto_stone/sien_pro_risotto_stone_bg_16.ckpt')

    # Update original weights in case some intermediate layers have been finetuned
    update_backbone_weights(backbone_weights, checkpoint_classifier)

    # Create backbone network
    backbone_network = build_backbone_network(backbone_model_config, backbone_weights)

    gesture_classifier = LogisticRegression(num_in=backbone_network.feature_dim,
                                            num_out=len(INT2LAB))
    gesture_classifier.load_state_dict(checkpoint_classifier)
    gesture_classifier.eval()

    # Concatenate feature extractor and met converter
    net = Pipe(backbone_network, gesture_classifier)

    postprocessors = [
        PostprocessClassificationOutput(INT2LAB, smoothing=4)
    ]

    display_ops = [
        sense.display.DisplayFPS(expected_camera_fps=net.fps,
                                 expected_inference_fps=net.fps / net.step_size),
        sense.display.DisplayTopKClassificationOutputs(top_k=1, threshold=0.1),
    ]
    display_results = sense.display.DisplayResults(title=title, display_ops=display_ops)

    # Run live inference
    controller = Controller(
        neural_network=net,
        post_processors=postprocessors,
        results_display=display_results,
        callbacks=[],
        camera_id=camera_id,
        path_in=path_in,
        path_out=path_out,
        use_gpu=use_gpu,
    )
    controller.run_inference()
