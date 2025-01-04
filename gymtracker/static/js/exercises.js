'use strict';

let ejercicios = [];

window.addEventListener('DOMContentLoaded', () => {
    fetch('/api/exercises') // URL del endpoint
        .then(response => response.json())
        .then(data => {
            for (const dato of data) {
                ejercicios.push(dato);
            };
            console.log(ejercicios);
        });
});

// Mostrar ejercicios en el modal
const mostrarEjercicios = () => {
    const contenedor = document.getElementById('container-exercises');
    console.log(contenedor);
    contenedor.innerHTML = '';
    console.log(ejercicios);
    ejercicios.forEach(ejercicio => {
        const div = document.createElement('div');
        div.className = 'modal__exercise-item'; 
        div.id = ejercicio.id;
        div.innerHTML = `
            <img class="modal__exercise-image" src="${ejercicio.ruta_imagen}" alt="Imagen de ${ejercicio.nombre}">
            
            <div class="modal__exercise-info">
                <h3 class="modal__exercise-title">${ejercicio.nombre}</h3>
                <p class="modal__exercise-primary">Músculo principal: <strong>${ejercicio.primary_muscle}</strong></p>
                <p class="modal__exercise-secondary">Músculos secundarios: ${ejercicio.secondary_muscle}</p>
            </div>`;

        
        div.addEventListener('click', () => {
            console.log(`Click en el ejercicio con ID ${ejercicio.id}`);
        });

        contenedor.appendChild(div);
    });
}

document.getElementById('open-modal').addEventListener('click', mostrarEjercicios);




