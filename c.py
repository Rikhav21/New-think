from flask import Flask, request, jsonify, render_template, Response
import numpy as np
import tensorflow as tf
import cv2
import mediapipe as mp
import os
import json

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('C:/rikhav_project/New-think/websit/ta.h5')
gestures = ['rock', 'paper', 'scissors']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Ensure directories exist
os.makedirs("rock", exist_ok=True)
os.makedirs("paper", exist_ok=True)
os.makedirs("scissors", exist_ok=True)

# Initialize score
user_score = 0
computer_score = 0

# Function to classify hand gesture
def classify_gesture(landmarks):
    data = np.array([landmarks])
    prediction = model.predict(data)
    gesture_id = np.argmax(prediction)
    return gestures[gesture_id]

# Function to save landmarks
def save_landmarks(gesture, landmarks):
    data = {
        "gesture": gesture,
        "landmarks": landmarks
    }
    filename = os.path.join(gesture, f"{gesture}_landmarks_{len(os.listdir(gesture)) + 1}.json")
    with open(filename, 'w') as f:
        json.dump(data, f)

@app.route('/')
def index():
    return render_template('index.html')

def generate_frames():
    cap = cv2.VideoCapture(0)
    while True:
        success, frame = cap.read()
        if not success:
            break
        else:
            # Convert the BGR image to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = hands.process(image)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    landmarks = [lm for lm in hand_landmarks.landmark]
                    landmarks = np.array([[lm.x, lm.y, lm.z] for lm in landmarks]).flatten()
                    gesture = classify_gesture(landmarks)
                    save_landmarks(gesture, landmarks)
                    cv2.putText(frame, gesture, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True, port=5001)