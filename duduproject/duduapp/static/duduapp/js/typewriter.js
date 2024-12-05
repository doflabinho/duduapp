document.addEventListener('DOMContentLoaded', () => {
    const typewriterElement = document.querySelector('.typewriter');

    const messages = [
        'Hello Bubu ❤️',
        'We have been together for 2 years!',
        'I made this app just for us.',
        'Hopefully you like it, it will include so many functions for us.',
        'Thank you for being my love!',
        '(Press on Bubu & Dudu to go back to homepage)'
    ];

    let currentMessageIndex = 0;

    function typeMessage(message, callback) {
        let index = 0;

        // Erstelle ein neues <div> für jede Nachricht
        const messageDiv = document.createElement('div');
        typewriterElement.appendChild(messageDiv);

        console.log(`Typing message: "${message}"`); // Debugging-Ausgabe

        const typingInterval = setInterval(() => {
            if (index < message.length) {
                messageDiv.innerHTML += message[index];
                index++;
            } else {
                clearInterval(typingInterval);
                // Verzögerung, bevor wir zur nächsten Nachricht übergehen
                setTimeout(callback, 1000);  // Warte 1 Sekunde, bevor die nächste Nachricht kommt
            }
        }, 150);  // 150ms pro Zeichen für langsames Tippen
    }

    function startTypingSequence() {
        console.log(`Current message index: ${currentMessageIndex}`); // Debugging-Ausgabe
        if (currentMessageIndex < messages.length) {
            typeMessage(messages[currentMessageIndex], () => {
                currentMessageIndex++;
                startTypingSequence();  // Nächste Nachricht starten
            });
        } else {
            console.log('All messages finished typing.'); // Debugging-Ausgabe
        }
    }

    startTypingSequence();
});












