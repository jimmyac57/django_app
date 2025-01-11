'use strict';
import { cerrarModal } from './modal.js';

// Arrays globales para manejar la selección
let ejercicios = [];
let ejerciciosSeleccionados = [];
let nombreEjerciciosSeleccionados = [];

// Mapa para guardar la referencia (idEjercicio -> inputHidden)
let inputMap = {};

// Al cargar la página, hacemos el fetch de los ejercicios
window.addEventListener('DOMContentLoaded', () => {
    fetch('/api/exercises') // Ajusta la ruta a tu backend
        .then(response => response.json())
        .then(data => {
            ejercicios = data; // Guardamos todos los ejercicios en el array global
            console.log('Ejercicios cargados:', ejercicios);
        })
        .catch(error => console.error('Error al cargar ejercicios:', error));
});

/**
 * Función para mostrar (o recargar) los ejercicios en el contenedor (modal).
 * Se llama al hacer clic en “Abrir Modal”.
 */
function mostrarEjercicios() {
    const contenedor = document.getElementById('container-exercises');
    contenedor.innerHTML = ''; // Limpia el contenedor

    ejercicios.forEach(ejercicio => {
        const div = document.createElement('div');
        div.className = 'modal__exercise-item';
        div.id = ejercicio.id;

        // Plantilla del contenido de cada ejercicio
        div.innerHTML = `
          <img class="modal__exercise-image" src="${ejercicio.ruta_imagen}" alt="Imagen de ${ejercicio.nombre}">
          <div class="modal__exercise-info">
              <h3 class="modal__exercise-title">${ejercicio.nombre}</h3>
              <p class="modal__exercise-primary">Músculo principal: <strong>${ejercicio.primary_muscle}</strong></p>
              <p class="modal__exercise-secondary">Músculos secundarios: ${ejercicio.secondary_muscle}</p>
          </div>
        `;

        // Al hacer clic en un ejercicio, lo seleccionamos o lo deseleccionamos
        div.addEventListener('click', () => {
            console.log(`Click en el ejercicio con ID ${ejercicio.id}`);

            if (ejerciciosSeleccionados.includes(ejercicio.id)) {
                // Si ya estaba seleccionado, lo quitamos
                div.classList.remove('selected');
                ejerciciosSeleccionados = ejerciciosSeleccionados.filter(id => id !== ejercicio.id);
                nombreEjerciciosSeleccionados = nombreEjerciciosSeleccionados.filter(nom => nom !== ejercicio.nombre);

                // Eliminamos también el input hidden correspondiente, si existe
                if (inputMap[ejercicio.id]) {
                    const form = document.getElementById('myForm');
                    form.removeChild(inputMap[ejercicio.id]);
                    delete inputMap[ejercicio.id];
                }
            } else {
                // Si NO estaba seleccionado, lo agregamos
                div.classList.add('selected');
                ejerciciosSeleccionados.push(ejercicio.id);
                nombreEjerciciosSeleccionados.push(ejercicio.nombre);

                // Creamos y agregamos el input hidden al formulario
                const form = document.getElementById('myForm');
                const hiddenInput = document.createElement('input');
                hiddenInput.type = 'hidden';
                hiddenInput.name = 'ejercicios[]'; // Al backend llegará como lista de IDs
                hiddenInput.value = ejercicio.id;
                form.appendChild(hiddenInput);

                // Guardamos la referencia en el mapa
                inputMap[ejercicio.id] = hiddenInput;
            }

            // Mostramos u ocultamos el botón "Guardar selección"
            mostrarOcultarBoton();

            console.log('IDs seleccionados:', ejerciciosSeleccionados);
            console.log('Nombres seleccionados:', nombreEjerciciosSeleccionados);
        });

        // Añadimos el div al contenedor
        contenedor.appendChild(div);
    });
}

// Escucha el clic en “Abrir Modal” para mostrar los ejercicios
document.getElementById('open-modal').addEventListener('click', mostrarEjercicios);

/**
 * Muestra la lista de ejercicios seleccionados en el contenedor “contenedor-seleccionados”.
 * Se llama al hacer clic en “Guardar selección”.
 */
function actualizarListaSeleccionados() {
    const contenedorSeleccionados = document.getElementById('contenedor-seleccionados');
    contenedorSeleccionados.innerHTML = ''; // Limpia lo anterior

    const ul = document.createElement('ul');

    nombreEjerciciosSeleccionados.forEach(nombre => {
        const li = document.createElement('li');
        li.textContent = nombre;
        ul.appendChild(li);
    });

    contenedorSeleccionados.appendChild(ul);
}

// Al hacer clic en “Guardar selección”, actualizamos la lista y (opcional) cerramos el modal
document.getElementById('btn-guardar-seleccion').addEventListener('click', () => {
    actualizarListaSeleccionados();
    // Aquí podrías cerrar el modal si lo tienes implementado con alguna librería
    cerrarModal();
    console.log('Selección guardada (en UI).');
});

/**
 * Muestra u oculta el botón “Guardar selección” en función de si hay ejercicios seleccionados.
 */
function mostrarOcultarBoton() {
    const btnGuardar = document.getElementById('btn-guardar-seleccion');
    if (nombreEjerciciosSeleccionados.length > 0) {
        btnGuardar.style.display = 'block';
    } else {
        btnGuardar.style.display = 'none';
    }
}