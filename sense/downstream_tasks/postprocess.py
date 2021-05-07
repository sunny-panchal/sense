from collections import deque

import numpy as np


class PostProcessor:

    def __init__(self, indices=None):
        self.indices = indices

    def filter(self, predictions):
        if predictions is None:
            return predictions

        if self.indices:
            if len(self.indices) == 1:
                index = self.indices[0]
                return predictions[index]
            else:
                return [predictions[index] for index in self.indices]
        return predictions

    def postprocess(self, prediction):
        raise NotImplementedError

    def __call__(self, predictions):
        return self.postprocess(self.filter(predictions))


class PostprocessClassificationOutput(PostProcessor):

    def __init__(self, mapping_dict, smoothing=1, **kwargs):
        super().__init__(**kwargs)
        self.mapping = mapping_dict
        self.smoothing = smoothing
        assert smoothing >= 1
        self.buffer = deque(maxlen=smoothing)

    def postprocess(self, classif_output):
        if classif_output is not None:
            self.buffer.append(classif_output)

        if self.buffer:
            classif_output_smoothed = sum(self.buffer) / len(self.buffer)
        else:
            classif_output_smoothed = np.zeros(len(self.mapping))

        indices = classif_output_smoothed.argsort()

        return {
            'sorted_predictions': [(self.mapping[index], classif_output_smoothed[index])
                                   for index in indices[::-1]]
        }


class PostprocessRepCounts(PostProcessor):

    def __init__(self, mapping_dict, threshold=0.4, **kwargs):
        super().__init__(**kwargs)
        self.mapping = mapping_dict
        self.threshold = threshold
        self.jumping_jack_counter = ExerciceSpecificRepCounter(
            mapping_dict,
            "counting - jumping_jacks_position=arms_down",
            "counting - jumping_jacks_position=arms_up",
            threshold)
        self.squats_counter = ExerciceSpecificRepCounter(
            mapping_dict,
            "counting - squat_position=high",
            "counting - squat_position=low",
            threshold)

    def postprocess(self, classif_output):
        if classif_output is not None:
            self.jumping_jack_counter.process(classif_output)
            self.squats_counter.process(classif_output)

        return {
            'counting': {
                "jumping_jacks": self.jumping_jack_counter.count,
                "squats": self.squats_counter.count
            }
        }


class ExerciceSpecificRepCounter:

    def __init__(self, mapping, position0, position1, threshold):
        self.threshold = threshold
        self.mapping = mapping
        self.inverse_mapping = {v: k for k, v in mapping.items()}
        self.position0 = position0
        self.position1 = position1
        self.count = 0
        self.position = 0

    def process(self, classif_output):
        if self.position == 0:
            if classif_output[self.inverse_mapping[self.position1]] > self.threshold:
                self.position = 1
        else:
            if classif_output[self.inverse_mapping[self.position0]] > self.threshold:
                self.position = 0
                self.count += 1


class EventCounter:
    """
    Count how many times a certain event, tied to a specific model class, occurs.

    This class implements a locking mechanism that prevents counting multiple occurrences
    when the class probability remains above the provided threshold for multiple consecutive
    time-steps. More precisely, the class probability should first decrease below half the
    provided threshold before another occurrence can be counted. In other words, this object
    detects and counts probability spikes.
    """

    def __init__(self, key, key_idx, threshold):
        """
        :param key:
            The name of the class that should be counted.
        :param key_idx:
            The index of the counted class in the predicted probability tensor.
        :param threshold:
            The threshold that should be reached for a probability spike to be counted.
        """
        self.key = key
        self.key_idx = key_idx
        self.threshold = threshold
        self.count = 0
        self.active = False

    def process(self, classif_output):
        if classif_output is not None:
            if self.active and classif_output[self.key_idx] < (self.threshold / 2.):
                self.active = False
            elif not self.active and classif_output[self.key_idx] > self.threshold:
                self.active = True
                self.count += 1
        return {self.key: self.count}


class PostprocessEventCounts(PostProcessor):
    """
    This class wraps a list of EventCounters and can therefore count how many times certain
    events occur.
    """

    def __init__(self, keys, label2int, label2threshold, **kwargs):
        """
        :param keys:
            The list of classes that should be counted.
        :param label2int:
            Dictionary that indicates the index of each class in the predicted probability tensor.
        :param label2threshold:
            Dictionary that indicates the threshold to use for each class.
        """
        super().__init__(**kwargs)
        self.event_counters = [
            EventCounter(key, label2int[key], label2threshold[key]) for key in keys
        ]

    def postprocess(self, classif_output):
        event_counts = {}
        for event_counter in self.event_counters:
            event_counts.update(event_counter.process(classif_output))

        return {'counting': event_counts}
