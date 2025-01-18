function padZero(num) {
    return num.toString().padStart(2, '0');
}

let ActualHour = new Date(); 

fetch('/api/currentHour/')
    .then(response => response.json())
    .then(data => {   
        ActualHour = new Date(data.current_hour); 
    })
    .catch(error => {
        console.error("Error al obtener la hora del servidor:", error);
    });

function updateActualHour() {
    ActualHour = new Date(ActualHour.getTime() + 1000); 
}


function updateElapsedTime() {
    const elapsedElements = document.querySelectorAll('[id^="elapsed-time-"]');

    elapsedElements.forEach(elapsedElement => {
        const startTime = new Date(elapsedElement.dataset.startTime); 
        const diff = ActualHour - startTime; 

        if (diff > 0) {
            const hours = padZero(Math.floor(diff / (1000 * 60 * 60)) % 24);
            const minutes = padZero(Math.floor(diff / (1000 * 60)) % 60);
            const seconds = padZero(Math.floor(diff / 1000) % 60);

            elapsedElement.innerHTML = `<strong>Elapsed Time:</strong> ${hours}:${minutes}:${seconds}`;
        } else {
            elapsedElement.innerHTML = "<strong>Elapsed Time:</strong> 00:00:00";
        }
    });
}

const startButton = document.getElementById('start-activity');
const activityForm = document.getElementById('activity-form');
if (startButton && activityForm) {
    startButton.addEventListener('click', () => {
        activityForm.style.display = 'block';
        newActivityForm.style.display = 'none';
    });
}

setInterval(updateActualHour, 1000);
setInterval(updateElapsedTime, 1000);

const newActivityForm = document.getElementById('new-activity-form');
const newActivityBtn =  document.getElementById('new-activity-btn');

newActivityBtn.addEventListener('click', () => {
    newActivityForm.style.display = 'block';
    activityForm.style.display = 'none';
});

document.querySelector('form').addEventListener('submit', function (event) {
    const selectField = document.getElementById('id_activity');
    if (!selectField.value) {
        event.preventDefault(); 
        selectField.classList.add('is-invalid');
        selectField.addEventListener('change', () => {
            selectField.classList.remove('is-invalid');
            selectField.parentElement.querySelector('.invalid-feedback').style.display = 'none';
        });
        selectField.parentElement.querySelector('.invalid-feedback').style.display = 'block';


    }
});
