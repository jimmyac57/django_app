'use strict';

const addExerciseButton = document.getElementById('open-modal');
const modal = document.getElementById('modal');
const closeModal = document.getElementById('close');

addExerciseButton.addEventListener('click', () => {
    console.log("abriendo modal");
    modal.style.display = 'flex';
});

closeModal.addEventListener('click', () => {
    console.log("cerrando modal");
    modal.style.display = 'none';
});

window.addEventListener('click', (event) => {
    if (event.target == modal) {
        console.log("cerrando modal");
        modal.style.display = 'none';
    }
  });

