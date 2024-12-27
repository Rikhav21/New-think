// This file contains the main JavaScript code for the rock-paper-scissors game.
// It initializes the game, handles user interactions, and manages game logic.

import { startWebcam, detectChoice } from './webcam.js';
import { animateComputerChoice } from './animation.js';
import { getRandomChoice, displayResult } from './utils/helpers.js';

const playerChoiceDisplay = document.getElementById('player-choice');
const computerChoiceDisplay = document.getElementById('computer-choice');
const resultDisplay = document.getElementById('result');
const startButton = document.getElementById('start-button');

document.addEventListener('DOMContentLoaded', () => {
    const userChoiceElement = document.getElementById('player-choice').querySelector('span');
    const resultElement = document.getElementById('result');
    const startGameButton = document.getElementById('start-game');
    const countdownElement = document.getElementById('countdown');

    startGameButton.addEventListener('click', async () => {
        console.log("Game started");
        await countdown();
        const userChoice = await detectHandGesture();
        userChoiceElement.innerText = userChoice;

        const computerChoice = await animateComputerChoice();
        const result = determineWinner(userChoice, computerChoice);
        resultElement.innerText = `Result: ${result}`;
        console.log("Game result: ", result);
    });
});

startButton.addEventListener('click', () => {
    startWebcam();
    detectPlayerChoice();
});

function detectPlayerChoice() {
    setInterval(() => {
        const playerChoice = detectChoice();
        if (playerChoice) {
            playerChoiceDisplay.textContent = `You chose: ${playerChoice}`;
            playRound(playerChoice);
        }
    }, 1000);
}

function playRound(playerChoice) {
    const computerChoice = getRandomChoice();
    computerChoiceDisplay.textContent = `Computer chose: ${computerChoice}`;
    animateComputerChoice(computerChoice);
    const result = determineWinner(playerChoice, computerChoice);
    displayResult(result);
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

async function countdown() {
    const countdownElement = document.getElementById('countdown');
    const steps = ['Rock', 'Paper', 'Scissors', 'Shoot'];
    for (let i = 0; i < steps.length; i++) {
        countdownElement.innerText = steps[i];
        await new Promise(resolve => setTimeout(resolve, 1000));
    }
    countdownElement.innerText = '';
}