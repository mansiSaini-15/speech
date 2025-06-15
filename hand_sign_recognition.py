import cv2
import numpy as np
import mediapipe as mp
import pyttsx3
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.8, min_tracking_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Sign detection functions
def sign_d(fingers, landmarks):
    return fingers == [0, 1, 1, 0, 0] and abs(landmarks[8].x - landmarks[12].x) > 0.05

def sign_g(fingers, landmarks):
    return fingers == [0, 1, 1, 0, 0] and abs(landmarks[8].x - landmarks[12].x) < 0.02

def sign_i(fingers, landmarks):
    return fingers == [0, 1, 0, 0, 0]  # Only index finger extended

def sign_o(fingers, landmarks):
    """ Detects 'O' by checking if the thumb and index fingertips are close together. """
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]

    # Calculate Euclidean distance between thumb tip and index tip
    distance = np.sqrt((thumb_tip.x - index_tip.x) ** 2 + (thumb_tip.y - index_tip.y) ** 2)

    return distance < 0.05  # Adjust this threshold based on testing

# Sign dictionary (including "O")
SIGNS = {
    "A": lambda fingers, landmarks: fingers == [0, 0, 0, 0, 0],  # Closed fist
    "B": lambda fingers, landmarks: fingers == [1, 1, 1, 1, 1],  # Open palm
    "C": lambda fingers, landmarks: fingers == [1, 0, 0, 0, 0],  # C shape with index and thumb
    "D": sign_d,  # Index and middle finger apart
    "E": lambda fingers, landmarks: fingers == [0, 0, 0, 0, 1],  # Slightly open fist
    "F": lambda fingers, landmarks: fingers == [1, 1, 0, 0, 0],  # Index and thumb touching
    "G": sign_g,  # Index and middle together
    "I": sign_i,  # Only index finger extended
    "O": sign_o,# Thumb and index tip touching (forming an "O")
}

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

last_detected = ""
last_time = time.time()
detection_delay = 1.0  # Time gap between detections in seconds

def detect_sign(finger_status, landmarks):
    for sign, condition in SIGNS.items():
        if callable(condition) and condition(finger_status, landmarks):
            return sign
    return ""

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        continue
    
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)
    
    detected_letter = ""
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers = [
                int(hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y),  # Index
                int(hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y),  # Middle
                int(hand_landmarks.landmark[16].y < hand_landmarks.landmark[14].y),  # Ring
                int(hand_landmarks.landmark[20].y < hand_landmarks.landmark[18].y)   # Pinky
            ]
            thumb_tip = hand_landmarks.landmark[4]
            thumb_ip = hand_landmarks.landmark[3]
            fingers.insert(0, int(thumb_tip.x > thumb_ip.x))  # Thumb position

            detected_letter = detect_sign(fingers, hand_landmarks.landmark)
    
    current_time = time.time()
    if detected_letter and detected_letter != last_detected and (current_time - last_time) > detection_delay:
        last_detected = detected_letter
        last_time = current_time
        engine.say(detected_letter)
        engine.runAndWait()
    
    if last_detected:
        cv2.putText(frame, f"Detected: {last_detected}", (50, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
    
    cv2.imshow("Hand Sign Recognition", frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
