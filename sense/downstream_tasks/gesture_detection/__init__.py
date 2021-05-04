LAB2INT = {
    "background": 0,
    "clockwise_rotation_offset=-0.5": 1,
    "Clockwise Rotation": 2,
    "clockwise_rotation_offset=0.5": 3,
    "counter-clockwise_rotation_offset=-0.5": 4,
    "Counter-clockwise Rotation": 5,
    "counter-clockwise_rotation_offset=0.5": 6,
    "invalid_gesture_offset=-0.5": 7,
    "invalid_gesture_offset=0": 8,
    "invalid_gesture_offset=0.5": 9,
    "swipe_down_offset=-0.5": 10,
    "Swipe Down": 11,
    "swipe_down_offset=0.5": 12,
    "swipe_left_with_left_hand_offset=-0.5": 13,
    "Swipe Left (left hand)": 14,
    "swipe_left_with_left_hand_offset=0.5": 15,
    "swipe_left_with_right_hand_offset=-0.5": 16,
    "Swipe Left (right hand)": 17,
    "swipe_left_with_right_hand_offset=0.5": 18,
    "swipe_right_with_left_hand_offset=-0.5": 19,
    "Swipe Right (left hand)": 20,
    "swipe_right_with_left_hand_offset=0.5": 21,
    "swipe_right_with_right_hand_offset=-0.5": 22,
    "Swipe Right (right hand)": 23,
    "swipe_right_with_right_hand_offset=0.5": 24,
    "swipe_up_offset=-0.5": 25,
    "Swipe Up": 26,
    "swipe_up_offset=0.5": 27,
    "thumb_down_offset=-0.5": 28,
    "Thumb Down": 29,
    "thumb_down_offset=0.5": 30,
    "thumb_up_offset=-0.5": 31,
    "Thumb Up": 32,
    "thumb_up_offset=0.5": 33,
    "zoom_in_with_full_hand_offset=-0.5": 34,
    "Zoom In": 35,
    "zoom_in_with_full_hand_offset=0.5": 36,
    "zoom_out_with_full_hand_offset=-0.5": 37,
    "Zoom Out": 38,
    "zoom_out_with_full_hand_offset=0.5": 39
}

INT2LAB = {value: key for key, value in LAB2INT.items()}

ENABLED_LABELS = [
    "Swipe Down",
    "Swipe Up",
    "Swipe Left (left hand)",
    "Swipe Left (right hand)",
    "Swipe Right (left hand)",
    "Swipe Right (right hand)",
    "Thumb Down",
    "Thumb Up",
]
LAB_THRESHOLDS = {key: 0.6 if key in ENABLED_LABELS else 1. for key in LAB2INT}
LAB_THRESHOLDS["Swipe Up"] = 0.8
