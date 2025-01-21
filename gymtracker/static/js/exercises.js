
// Array para almacenar los ejercicios seleccionados y añadidos
let selectedExercises = [];

// Referencia al botón de "Add Selected Exercises"
const addSelectedButton = document.getElementById('btn-guardar-seleccion');

// Función para actualizar el texto del botón
function updateSelectedButtonText() {
    const count = selectedExercises.length; // Número de ejercicios seleccionados
    if (count > 0) {
        addSelectedButton.textContent = `Add Selected Exercises (${count})`;
    } else {
        addSelectedButton.textContent = 'Add Selected Exercises';
    }
}

// Escuchar clicks en los ejercicios dentro del modal
document.getElementById('container-exercises').addEventListener('click', (event) => {
    // Buscar el contenedor principal del ejercicio clicado
    const exerciseItem = event.target.closest('.exercise-item');
    if (exerciseItem) {
        const exerciseId = exerciseItem.getAttribute('data-id');
        const exerciseName = exerciseItem.querySelector('.exercise-name').textContent.trim();

        // Verificar si el ejercicio ya está seleccionado
        const index = selectedExercises.findIndex(exercise => exercise.id === exerciseId);
        if (index >= 0) {
            // Si ya está seleccionado, lo quitamos del array
            selectedExercises.splice(index, 1);
            exerciseItem.classList.remove('active', 'border-primary', 'bg-light'); // Cambiar estilo al desmarcar
        } else {
            // Si no está seleccionado, lo añadimos al array
            selectedExercises.push({ id: exerciseId, name: exerciseName });
            exerciseItem.classList.add('active', 'border-primary', 'bg-light'); // Cambiar estilo al marcar
        }

        // Actualizar el texto del botón
        updateSelectedButtonText();
    }
});

// Añadir ejercicios seleccionados al contenedor al presionar "Add Selected Exercises"
addSelectedButton.addEventListener('click', () => {
    const selectedContainer = document.getElementById('contenedor-seleccionados');

    // Recorrer los ejercicios seleccionados
    selectedExercises.forEach(exercise => {
        // Verificar si ya fue añadido previamente al formulario
        const existingInput = document.querySelector(`input[value="${exercise.id}"]`);
        if (!existingInput) {
            // Añadir al contenedor si no existe
            const selectedItem = document.createElement('div');
            selectedItem.className = 'selected-exercise mb-2 d-flex align-items-center justify-content-between';
            selectedItem.innerHTML = `
                <input type="hidden" name="ejercicios[]" value="${exercise.id}">
                <span>${exercise.name}</span>
                <button type="button" class="btn btn-danger btn-sm ms-2">Remove</button>
            `;
            selectedContainer.appendChild(selectedItem);
        }
    });

    // Eliminar los ejercicios desmarcados del contenedor
    const selectedContainerItems = Array.from(selectedContainer.children);
    selectedContainerItems.forEach(item => {
        const input = item.querySelector('input');
        const exerciseId = input.value;

        // Si el ejercicio no está en `selectedExercises`, lo eliminamos del contenedor
        if (!selectedExercises.some(exercise => exercise.id === exerciseId)) {
            item.remove();
        }
    });

    // Actualizar el texto del botón después de agregar
    updateSelectedButtonText();
});

// Restaurar el estilo de los ejercicios seleccionados al abrir el modal
document.getElementById('open-modal').addEventListener('click', () => {
    const exerciseItems = document.querySelectorAll('#container-exercises .exercise-item');
    exerciseItems.forEach(item => {
        const exerciseId = item.getAttribute('data-id');
        if (selectedExercises.some(exercise => exercise.id === exerciseId)) {
            item.classList.add('active', 'border-primary', 'bg-light'); // Restaurar el estilo de los seleccionados
        } else {
            item.classList.remove('active', 'border-primary', 'bg-light'); // Asegurarse de que los no seleccionados no tengan el estilo
        }
    });

    // Actualizar el texto del botón cuando se abre el modal
    updateSelectedButtonText();
});

// Eliminar ejercicios del contenedor seleccionado
document.getElementById('contenedor-seleccionados').addEventListener('click', (event) => {
    if (event.target.tagName === 'BUTTON') {
        const parentDiv = event.target.parentNode;
        const input = parentDiv.querySelector('input');
        const exerciseId = input.value;

        // Remover el ejercicio del array `selectedExercises`
        selectedExercises = selectedExercises.filter(exercise => exercise.id !== exerciseId);

        // Remover el elemento del contenedor
        parentDiv.remove();

        // Actualizar el estilo en el modal si está abierto
        const exerciseItem = document.querySelector(`#container-exercises .exercise-item[data-id="${exerciseId}"]`);
        if (exerciseItem) {
            exerciseItem.classList.remove('active', 'border-primary', 'bg-light');
        }

        // Actualizar el texto del botón
        updateSelectedButtonText();
    }
});

document.getElementById('filter-muscle').addEventListener('change', function () {
    const selectedMuscle = this.value.toLowerCase(); // Valor del filtro en minúsculas
    const exercises = document.querySelectorAll('#container-exercises .exercise-item');

    exercises.forEach(exercise => {
        const muscle = (exercise.getAttribute('data-muscle') || '').toLowerCase(); // Atributo data-muscle en minúsculas
        // Coincide completamente o contiene el músculo seleccionado
        if (selectedMuscle === 'all' || muscle.includes(selectedMuscle)) {
            exercise.classList.add('d-flex'); // Muestra el ejercicio
            exercise.classList.remove('d-none');
        } else {
            exercise.classList.remove('d-flex'); // Oculta el ejercicio
            exercise.classList.add('d-none');
        }
    });
});
