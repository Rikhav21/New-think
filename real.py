import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import time

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
model = tf.keras.models.load_model('gesture_model.h5')
gestures = ['rock', 'paper', 'scissors']
def classify(landmarks):
    data = np.array([landmarks])
    prediction = model.predict(data)
    id = np.argmax(prediction)
    return gestures[id]
def captre():
    cap = cv2.VideoCapture(0)
    start = time.time()
    Detect = None
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(frame_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                landmarks = [lm.x for lm in hand_landmarks.landmark] + \
                            [lm.y for lm in hand_landmarks.landmark] + \
                            [lm.z for lm in hand_landmarks.landmark]
                Detect = classify(landmarks)

        cv2.imshow('Hand Gesture Classification', frame)
        if time.time() - start > 5:
            break
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
    if Detect:
        print(f"Detected Gesture: {Detect}")
    else:
        print("No hand detected")
if __name__ == "__main__":
    captre()