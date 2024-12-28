// This file contains the main JavaScript code for the rock-paper-scissors game.
// It initializes the game, handles user interactions, and manages game logic.

import { detectHandGesture } from './webcam.js';
import { animateComputerChoice } from './animation.js';

document.addEventListener('DOMContentLoaded', () => {
    const userChoiceElement = document.getElementById('player-choice').querySelector('span');
    const resultElement = document.getElementById('result');
    const startGameButton = document.getElementById('start-game');
    const countdownElement = document.getElementById('countdown');

    startGameButton.addEventListener('click', async () => {
        console.log("Start Game button clicked");
        await countdown();
        console.log("Countdown finished");

        const userChoice = await detectHandGesture();
        console.log("User choice detected:", userChoice);
        userChoiceElement.innerText = userChoice;

        const computerChoice = await window.animateComputerChoice();
        console.log("Computer choice animated:", computerChoice);

        const result = determineWinner(userChoice, computerChoice);
        console.log("Game result determined:", result);
        resultElement.innerText = `Result: ${result}`;
    });
});

async function countdown() {
    const countdownElement = document.getElementById('countdown');
    const steps = ['Rock', 'Paper', 'Scissors', 'Shoot'];
    for (let i = 0; i < steps.length; i++) {
        countdownElement.innerText = steps[i];
        console.log("Countdown step:", steps[i]);
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    countdownElement.innerText = '';
}

function determineWinner(userChoice, computerChoice) {
    const choices = ['Rock', 'Paper', 'Scissors'];
    const userIndex = choices.indexOf(userChoice);
    const computerIndex = choices.indexOf(computerChoice);

    if (userIndex === computerIndex) {
        return 'Draw';
    } else if ((userIndex + 1) % 3 === computerIndex) {
        return 'Computer Wins';
    } else {
        return 'You Win';
    }
}

// Make the function available globally
window.detectHandGesture = detectHandGesture;