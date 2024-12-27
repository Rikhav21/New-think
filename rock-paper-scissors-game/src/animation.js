function animateComputerChoice() {
    const choices = ['Rock', 'Paper', 'Scissors'];
    let index = 0;
    const interval = setInterval(() => {
        document.getElementById('computer-choice').querySelector('span').innerText = choices[index];
        index = (index + 1) % choices.length;
    }, 100);

    return new Promise(resolve => {
        setTimeout(() => {
            clearInterval(interval);
            const finalChoice = choices[Math.floor(Math.random() * choices.length)];
            document.getElementById('computer-choice').querySelector('span').innerText = finalChoice;
            console.log("Computer's final choice: ", finalChoice);
            resolve(finalChoice);
        }, 2000);
    });
}