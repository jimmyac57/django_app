'use strict';

const addExerciseButton = document.getElementById('open-modal');
const modal = document.getElementById('modal');
const closeModal = document.getElementById('close');

addExerciseButton.addEventListener('click', () => {
    abrirModal();
});

closeModal.addEventListener('click', () => {
    cerrarModal();
});

window.addEventListener('click', (event) => {
    if (event.target == modal) {
        cerrarModal();
    }
});

export function abrirModal() {
    console.log("abriendo modal");
    modal.style.display = 'flex';
}

export function cerrarModal() {
    console.log("cerrando modal");
    modal.style.display = 'none';
}

