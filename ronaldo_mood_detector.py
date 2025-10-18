import cv2
import numpy as np
import os
import mediapipe as mp
from enum import Enum

from fontTools.unicodedata.Mirrored import MIRRORED

WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 480
RONALDO_IMAGES = "ronaldo_images"
MIRROR_CAMERA = True  # Optional: mirror the camera feed for a “selfie view”.

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1,
                                  min_detection_confidence=0.5,
                                  min_tracking_confidence=0.5)

mp_hands = mp.solutions.hands
hands_detector = mp_hands.Hands(max_num_hands=2,
                                min_detection_confidence=0.5,
                                min_tracking_confidence=0.5)

class RonaldoState(Enum):
    SERIOUS = 1
    SIUU = 2
    FIVE_CHAMPIONS = 3

def setup_camera():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise RuntimeError("Cannot open webcam")
    return cap

def load_emoji(state: RonaldoState):
    filename = f"{state.name.lower()}.jpg"
    emoji_path = os.path.join(RONALDO_IMAGES, filename)
    if not os.path.exists(emoji_path):
        emoji_path = os.path.join(RONALDO_IMAGES, "serious.jpg")

    emoji = cv2.imread(emoji_path)
    if emoji is None:
        raise FileNotFoundError(f"Missing emoji image for {state.name}")

    emoji = cv2.resize(emoji, (WINDOW_WIDTH // 2, WINDOW_HEIGHT))
    return emoji


def is_hand_five(hand_landmarks, is_right_hand):
    extended_fingers = 0

    # For the 4 main fingers, we just check that the tip is above the DIP joint
    fingers_tip = [8, 12, 16, 20]
    fingers_dip = [7, 11, 15, 19]
    for tip_idx, dip_idx in zip(fingers_tip, fingers_dip):
        if hand_landmarks.landmark[tip_idx].y < hand_landmarks.landmark[dip_idx].y:
            extended_fingers += 1

    # For the thumb, check that it points outward relative to the IP joint
    thumb_tip = hand_landmarks.landmark[4]
    thumb_ip = hand_landmarks.landmark[3]

    if is_right_hand and thumb_tip.x > thumb_ip.x:
        extended_fingers += 1
    elif not is_right_hand and thumb_tip.x < thumb_ip.x:
        extended_fingers += 1

    return extended_fingers == 5


def detect_status(frame):
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # FIVE_CHAMPIONS state
    results_hands = hands_detector.process(image_rgb)
    if results_hands.multi_hand_landmarks:
        for hand_landmarks, handedness in zip(results_hands.multi_hand_landmarks, results_hands.multi_handedness):
            # handedness.classification[0].label is "Right" or "Left"
            is_right = handedness.classification[0].label == "Right"
            # Invert if camera is mirrored
            if MIRROR_CAMERA:
                is_right = not is_right
            if is_hand_five(hand_landmarks, is_right):
                return RonaldoState.FIVE_CHAMPIONS

    # SIUU state
    results_face = face_mesh.process(image_rgb)
    if results_face.multi_face_landmarks:
        face_landmarks = results_face.multi_face_landmarks[0].landmark
        left_corner = face_landmarks[61]
        right_corner = face_landmarks[291]
        upper_lip = face_landmarks[13]
        lower_lip = face_landmarks[14]

        mouth_width = ((right_corner.x - left_corner.x) ** 2 +
                       (right_corner.y - left_corner.y) ** 2) ** 0.5
        mouth_height = ((lower_lip.x - upper_lip.x) ** 2 +
                        (lower_lip.y - upper_lip.y) ** 2) ** 0.5

        if mouth_width > 0:
            mouth_aspect_ratio = mouth_height / mouth_width
            if mouth_aspect_ratio > 0.35:
                return RonaldoState.SIUU

    # Default state
    return RonaldoState.SERIOUS

def update_display(frame, state):
    if MIRROR_CAMERA:
        frame = cv2.flip(frame, 1)
    frame_resized = cv2.resize(frame, (WINDOW_WIDTH // 2, WINDOW_HEIGHT))

    emoji_img = load_emoji(state)
    combined = np.hstack((frame_resized, emoji_img))

    cv2.putText(combined, "Camera", (50, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(combined, f"Ronaldo Mood: {state.name}",
                (WINDOW_WIDTH // 2 + 50, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.putText(combined, "Press 'q' to quit", (20, combined.shape[0]-20),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("Ronaldo Detector", combined)


def camera_loop():
    cap = setup_camera()

    while True:
        success, frame = cap.read()
        if not success:
            continue

        ronaldo_state = detect_status(frame)
        update_display(frame, ronaldo_state)

        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    camera_loop()

if __name__ == "__main__":
    main()
