import cv2
import mediapipe as mp
import numpy as np
import tensorflow as tf
import time
import random
from flask import Flask, render_template_string, Response, request, jsonify

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

def generate_frames():
    """Generate video frames for webcam and process hand gestures."""
    global detecting, countdown_start, final_result, computer_choice
    cap = cv2.VideoCapture(0)
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Flip and convert frame to RGB
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Handle countdown and detection
        if detecting:
            elapsed_time = time.time() - countdown_start
            remaining_time = max(0, 3 - int(elapsed_time))  # 3-second countdown
            if remaining_time > 0:
                # Display countdown on the video feed
                cv2.putText(frame, f"Get Ready: {remaining_time}", (150, 200), 
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 255), 4, cv2.LINE_AA)
            elif elapsed_time < 4:  # Detection phase for 1 second
                results = hands.process(frame_rgb)
                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                        landmarks = [lm.x for lm in hand_landmarks.landmark] + \
                                    [lm.y for lm in hand_landmarks.landmark] + \
                                    [lm.z for lm in hand_landmarks.landmark]
                        final_result = classify(landmarks)
                        cv2.putText(frame, f"Detected: {final_result}", (10, 50), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                # Stop detection, generate computer choice, and determine the winner
                detecting = False
                computer_choice = random.choice(gestures)
                determine_winner(final_result, computer_choice)

        # If not detecting, show the result
        if not detecting and final_result:
            cv2.putText(frame, f"Your Gesture: {final_result}", (10, 50), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            cv2.putText(frame, f"Computer: {computer_choice}", (10, 100), 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 2, cv2.LINE_AA)

        # Encode frame for streaming
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        # Yield frame for live stream
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    cap.release()
    cv2.destroyAllWindows()

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
        </style>
        <script>
            function startGame() {
                fetch('/start', { method: 'POST' }).then(() => {
                    // Poll for scores and update them dynamically
                    setInterval(() => {
                        fetch('/scores')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('userScore').textContent = data.user_wins;
                            document.getElementById('computerScore').textContent = data.computer_wins;
                        });
                    }, 1000);
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
            <img src="/video_feed" width="640" height="480">
        </div>
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

@app.route('/video_feed')
def video_feed():
    """Video feed route for live webcam stream."""
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
