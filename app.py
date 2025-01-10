import os
import random
import base64
import cv2
import numpy as np
from flask import Flask, render_template_string, jsonify, request, Response
import tensorflow as tf
import mediapipe as mp
import time

# Initialize Flask app
app = Flask(__name__)

# Load model and initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=1, 
                       min_detection_confidence=0.5, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
model = tf.keras.models.load_model('ta.h5')
gestures = ['rock', 'paper', 'scissors']

# Global state to control game logic
detecting = False
countdown_start = None
final_result = None
computer_choice = None
user_wins = 0
computer_wins = 0

def classify(landmarks):
    """Classify the hand landmarks into gestures."""
    data = np.array([landmarks])
    prediction = model.predict(data)
    gesture_id = np.argmax(prediction)
    return gestures[gesture_id]

def determine_winner(user_choice, computer_choice):
    """Determine the winner of Rock-Paper-Scissors."""
    global user_wins, computer_wins
    if user_choice == computer_choice:
        return "It's a tie!"
    elif (user_choice == "rock" and computer_choice == "scissors") or \
         (user_choice == "paper" and computer_choice == "rock") or \
         (user_choice == "scissors" and computer_choice == "paper"):
        user_wins += 1
        return "You win!"
    else:
        computer_wins += 1
        return "Computer wins!"

@app.route('/')
def index():
    """Home page with live video stream and button to start detection."""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Rock Paper Scissors</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                background-color: #f0f8ff;
            }
            h1 {
                color: #333;
                margin-top: 20px;
            }
            .scoreboard {
                display: flex;
                justify-content: center;
                gap: 20px;
                margin-top: 20px;
                font-size: 1.2em;
            }
            .score {
                padding: 20px;
                border-radius: 10px;
                background: #87ceeb;
                color: #fff;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            button {
                padding: 10px 20px;
                font-size: 1.2em;
                color: white;
                background: #0078d7;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                margin: 20px 0;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
            button:hover {
                background: #005a9e;
            }
            video {
                border: 1px solid #ccc;
                border-radius: 10px;
                width: 640px;
                height: 480px;
            }
        </style>
        <script>
            let videoStream;
            let intervalId;

            async function startGame() {
                try {
                    videoStream = await navigator.mediaDevices.getUserMedia({ video: true });
                    const videoElement = document.getElementById('video');
                    videoElement.srcObject = videoStream;
                    videoElement.play();

                    // Capture frames and send to server for processing
                    intervalId = setInterval(captureFrame, 1000);

                    // Poll for scores and update them dynamically
                    setInterval(() => {
                        fetch('/scores')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('userScore').textContent = data.user_wins;
                            document.getElementById('computerScore').textContent = data.computer_wins;
                        });
                    }, 1000);
                } catch (error) {
                    console.error('Error accessing webcam:', error);
                }
            }

            function captureFrame() {
                const videoElement = document.getElementById('video');
                const canvas = document.createElement('canvas');
                canvas.width = videoElement.videoWidth;
                canvas.height = videoElement.videoHeight;
                const context = canvas.getContext('2d');
                context.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
                const frame = canvas.toDataURL('image/jpeg');

                fetch('/process_frame', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ frame: frame })
                })
                .then(response => response.json())
                .then(data => {
                    if (data.result) {
                        document.getElementById('result').textContent = `Detected: ${data.result}`;
                    }
                })
                .catch(error => {
                    console.error('Error processing frame:', error);
                });
            }
        </script>
    </head>
    <body>
        <h1>Rock-Paper-Scissors</h1>
        <div class="scoreboard">
            <div class="score">
                <h2 id="userScore">0</h2>
                <p>Your Wins</p>
            </div>
            <div class="score">
                <h2 id="computerScore">0</h2>
                <p>Computer Wins</p>
            </div>
        </div>
        <button onclick="startGame()">Start Game</button>
        <div class="video-container">
            <video id="video" autoplay></video>
        </div>
        <div id="result"></div>
    </body>
    </html>
    """
    return render_template_string(html)

@app.route('/start', methods=['POST'])
def start_game():
    """Start the countdown and detection."""
    global detecting, countdown_start, final_result, computer_choice
    detecting = True
    countdown_start = time.time()
    final_result = None
    computer_choice = None
    return '', 204  # No content response

@app.route('/scores', methods=['GET'])
def get_scores():
    """Return the current scores as JSON."""
    return jsonify({'user_wins': user_wins, 'computer_wins': computer_wins})

@app.route('/process_frame', methods=['POST'])
def process_frame():
    """Process the frame sent from the client."""
    data = request.json
    frame_data = data['frame'].split(',')[1]
    frame = np.frombuffer(base64.b64decode(frame_data), dtype=np.uint8)
    
    if frame.size == 0:
        return jsonify({'result': None, 'error': 'Empty frame data'})

    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
    
    if frame is None:
        return jsonify({'result': None, 'error': 'Failed to decode frame'})

    # Process the frame with Mediapipe and classify the gesture
    results = hands.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            landmarks = [lm.x for lm in hand_landmarks.landmark] + \
                        [lm.y for lm in hand_landmarks.landmark] + \
                        [lm.z for lm in hand_landmarks.landmark]
            final_result = classify(landmarks)
            return jsonify({'result': final_result})

    return jsonify({'result': None})

if __name__ == "__main__":
    app.run(debug=True, port=6123)
