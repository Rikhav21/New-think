import { Hands } from '@mediapipe/hands';
import { Camera } from '@mediapipe/camera_utils';

const video = document.getElementById('webcam');
const canvas = document.getElementById('output-canvas');
const context = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        console.log("Webcam stream started");
    })
    .catch(err => {
        console.error("Error accessing webcam: ", err);
    });

const hands = new Hands({
    locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`
});

hands.setOptions({
    maxNumHands: 1,
    modelComplexity: 1,
    minDetectionConfidence: 0.5,
    minTrackingConfidence: 0.5
});

hands.onResults(onResults);

const camera = new Camera(video, {
    onFrame: async () => {
        await hands.send({ image: video });
    },
    width: 640,
    height: 480
});
camera.start();

function onResults(results) {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    if (results.multiHandLandmarks && results.multiHandLandmarks.length > 0) {
        const landmarks = results.multiHandLandmarks[0];
        console.log("Hand landmarks: ", landmarks);
        const gesture = classifyGesture(landmarks);
        console.log("Classified gesture: ", gesture);
        return gesture;
    } else {
        console.log("No hand detected");
        return 'No hand detected';
    }
}

function classifyGesture(landmarks) {
    // Placeholder logic for classifying gestures
    // Replace this with actual gesture classification logic
    const randomChoice = ['Rock', 'Paper', 'Scissors'][Math.floor(Math.random() * 3)];
    console.log("Classified gesture: ", randomChoice);
    return randomChoice;
}

export async function detectHandGesture() {
    // This function will be called by app.js to get the detected gesture
    return new Promise((resolve) => {
        hands.onResults((results) => {
            const gesture = onResults(results);
            resolve(gesture);
        });
    });
}

function captureImage() {
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/png');
    console.log("Captured image: ", imageData);
    return imageData;
}

function identifyChoice(frame) {
    // Logic to process the frame and identify rock, paper, or scissors
    // This is a placeholder for the actual implementation
    return 'rock'; // Example return value
}

function startWebcam() {
    navigator.mediaDevices.getUserMedia({ video: true }).then(() => {
        setInterval(() => {
            const frame = captureImage();
            const choice = identifyChoice(frame);
            console.log('Player choice:', choice);
        }, 1000); // Capture frame every second
    });
}

startWebcam();