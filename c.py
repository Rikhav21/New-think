import cv2
import mediapipe as mp
import json
import os
from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
app = Flask(__name__)
model = tf.keras.models.load_model('gesture_model.h5')
gestures = ['rock', 'paper', 'scissors']
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
user_score = 0
computer_score = 0
os.makedirs("rock", exist_ok=True)
os.makedirs("paper", exist_ok=True)
os.makedirs("scissors", exist_ok=True)
def save_landmarks(gesture, landmarks):
    data = {
        "gesture": gesture,
        "landmarks": landmarks
    }
    filename = os.path.join(gesture, f"{gesture}_landmarks_{len(os.listdir(gesture)) + 1}.json")
    with open(filename, 'w') as f:
        json.dump(data, f)
    print(f"Saved {gesture} landmarks to {filename}")
def classify_gesture(landmarks):
    data = np.array([landmarks])
    prediction = model.predict(data)
    gesture_id = np.argmax(prediction)
    return gestures[gesture_id]
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/classify', methods=['POST'])
def classify():
    global user_score, computer_score
    data = request.json
    landmarks = data['landmarks']
    user_gesture = classify_gesture(landmarks)
    computer_gesture = np.random.choice(gestures)
    
    if user_gesture == computer_gesture:
        result = 'tie'
    elif (user_gesture == 'rock' and computer_gesture == 'scissors') or \
         (user_gesture == 'paper' and computer_gesture == 'rock') or \
         (user_gesture == 'scissors' and computer_gesture == 'paper'):
        result = 'win'
        user_score += 1
    else:
        result = 'lose'
        computer_score += 1
    return jsonify({
        'user_gesture': user_gesture,
        'computer_gesture': computer_gesture,
        'result': result,
        'user_score': user_score,
        'computer_score': computer_score
    })
def capture_hand_landmarks():
    cap = cv2.VideoCapture(0)
    current_gesture = None
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
                landmarks = [{"x": lm.x, "y": lm.y, "z": lm.z} for lm in hand_landmarks.landmark]
                if current_gesture:
                    save_landmarks(current_gesture, landmarks)
                    current_gesture = None
        cv2.imshow('Hand Gesture Capture', frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('r'):
            current_gesture = 'rock'
            print("Capturing Rock gesture")
        elif key == ord('p'):
            current_gesture = 'paper'
            print("Capturing Paper gesture")
        elif key == ord('s'):
            current_gesture = 'scissors'
            print("Capturing Scissors gesture")
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    app.run(debug=True)
    capture_hand_landmarks()