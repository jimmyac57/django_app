function padZero(num) {
    return num.toString().padStart(2, '0');
}

function updateClock() {
    const now = new Date();
    const hours = padZero(now.getHours());
    const minutes = padZero(now.getMinutes());
    const seconds = padZero(now.getSeconds());
    document.getElementById('clock').textContent = `${hours}:${minutes}:${seconds}`;
}

// Calcular tiempo transcurrido
function updateElapsedTime() {
    const elapsedElements = document.querySelectorAll('[id^="elapsed-time-"]');
    elapsedElements.forEach(elapsedElement => {
        const startTime = new Date(elapsedElement.dataset.startTime); 
        const now = new Date();
        const diff = new Date(now - startTime); 

        const hours = padZero(diff.getUTCHours());
        const minutes = padZero(diff.getUTCMinutes());
        const seconds = padZero(diff.getUTCSeconds());

        elapsedElement.textContent = `Tiempo transcurrido: ${hours}:${minutes}:${seconds}`;
    });
}

const startButton = document.getElementById('start-activity');
const activityForm = document.getElementById('activity-form');
if (startButton && activityForm) {
    startButton.addEventListener('click', () => {
        activityForm.style.display = 'block';
    });
}

setInterval(updateClock, 1000);
setInterval(updateElapsedTime, 1000);

updateClock();
updateElapsedTime();