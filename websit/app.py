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

# Initialize score
user_score = 0
computer_score = 0

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

if __name__ == "__main__":
    app.run(debug=True, port=5001)