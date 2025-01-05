from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model("C:/rikhav_project/New-think/websit/ta.h5")
gestures = ['rock', 'paper', 'scissors']

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
    else:
        result = 'lose'

    return jsonify({
        'user_gesture': user_gesture,
        'computer_gesture': computer_gesture,
        'result': result
    })

if __name__ == "__main__":
    app.run(debug=True, port=5001)
