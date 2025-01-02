from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
import mediapipe as mp

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('gesture_model.h5')

# Define the gestures
gestures = ['rock', 'paper', 'scissors']

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Function to classify hand gesture
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
    data = request.json
    landmarks = data['landmarks']
    gesture = classify_gesture(landmarks)
    return jsonify({'gesture': gesture})

if __name__ == "__main__":
    app.run(debug=True)