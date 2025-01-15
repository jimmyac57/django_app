function padZero(num) {
    return num.toString().padStart(2, '0');
}

function updateClock() {
    // Hora actual en la zona horaria local
    const now = new Date();
    const formatter = new Intl.DateTimeFormat('es-CL', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: false,
        timeZone: 'America/Santiago'
    });
    const formattedTime = formatter.format(now);
    document.getElementById('clock').textContent = formattedTime;
}

// Calcular tiempo transcurrido
function updateElapsedTime() {
    const elapsedElements = document.querySelectorAll('[id^="elapsed-time-"]');
    elapsedElements.forEach(elapsedElement => {
        const utcStartTime = new Date(elapsedElement.dataset.startTime); // UTC desde la base de datos
        const santiagoStartTime = new Date(utcStartTime.toLocaleString('en-US', { timeZone: 'America/Santiago' })); // Convertir a America/Santiago
        const now = new Date();
        const santiagoNow = new Date(now.toLocaleString('en-US', { timeZone: 'America/Santiago' })); // Hora actual en America/Santiago
        const diff = new Date(santiagoNow - santiagoStartTime); // Diferencia de tiempo

        const hours = padZero(diff.getUTCHours());
        const minutes = padZero(diff.getUTCMinutes());
        const seconds = padZero(diff.getUTCSeconds());

        elapsedElement.textContent = `Tiempo transcurrido: ${hours}:${minutes}:${seconds}`;
    });
}

// Mostrar el formulario al iniciar una nueva actividad
const startButton = document.getElementById('start-activity');
const activityForm = document.getElementById('activity-form');
if (startButton && activityForm) {
    startButton.addEventListener('click', () => {
        activityForm.style.display = 'block';
    });
}

// Actualizar el reloj y el tiempo transcurrido cada segundo
setInterval(updateClock, 1000);
setInterval(updateElapsedTime, 1000);

// Inicializar valores al cargar la página
updateClock();
updateElapsedTime();
