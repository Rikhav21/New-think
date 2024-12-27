const video = document.getElementById('webcam');
const canvas = document.createElement('canvas');
const context = canvas.getContext('2d');

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        console.log("Webcam stream started");
    })
    .catch(err => {
        console.error("Error accessing webcam: ", err);
    });

export async function detectHandGesture() {
    const video = document.getElementById('webcam');
    const model = await handpose.load();
    console.log("Handpose model loaded");

    const predictions = await model.estimateHands(video);
    if (predictions.length > 0) {
        const landmarks = predictions[0].landmarks;
        console.log("Hand landmarks: ", landmarks);
        return classifyGesture(landmarks);
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