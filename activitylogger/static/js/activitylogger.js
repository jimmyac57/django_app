function padZero(num) {
    return num.toString().padStart(2, '0');
}


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

        console.log("Start Time (data-start-time):", elapsedElement.dataset.startTime);
        console.log("Start Time (parsed):", startTime);
        console.log("Hora actual:", now);
        console.log("Diferencia en milisegundos:", now - startTime);
        console.log("Tiempo transcurrido: ", `${hours}:${minutes}:${seconds}`);
    });
}

const startButton = document.getElementById('start-activity');
const activityForm = document.getElementById('activity-form');
if (startButton && activityForm) {
    startButton.addEventListener('click', () => {
        activityForm.style.display = 'block';

        console.log("Formulario de actividad mostrado.");
    });
}


setInterval(updateElapsedTime, 1000);

updateElapsedTime();

fetch('/api/currentHour/')
    .then(response => response.json())
    .then(data => console.log(data));