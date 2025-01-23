document.addEventListener("DOMContentLoaded", () => {
    const deletedSets = new Set(); // Almacena los IDs de las series eliminadas

    // Función para actualizar los números de las series
    const updateSetNumbers = (table) => {
        const rows = table.querySelectorAll("tr.set-item");
        rows.forEach((row, index) => {
            const setNumber = index + 1; // Calcular el número de la serie
            const setNumberCell = row.querySelector(".set-number");
            setNumberCell.textContent = setNumber; // Actualizar el número visualmente
            row.setAttribute("data-set-number", setNumber); // Actualizar el número en el atributo
        });
    };

    // Eliminar un ejercicio si no tiene series
    const removeExerciseIfEmpty = (exercise) => {
        const sets = exercise.querySelectorAll(".set-item");
        if (sets.length === 0) {
            exercise.remove(); // Eliminar el ejercicio del DOM
        }
    };

    // Añadir nueva serie
    document.querySelectorAll(".add-set").forEach(button => {
        button.addEventListener("click", () => {
            const setTable = button.previousElementSibling.querySelector("tbody");
            const newRow = document.createElement("tr");
            newRow.classList.add("set-item");
            newRow.innerHTML = `
                <td class="set-number"></td> <!-- Número de serie dinámico -->
                <td>
                    <input 
                        type="number" 
                        class="form-control form-control-sm set-weight" 
                        value="0" 
                        step="0.1">
                </td>
                <td>
                    <input 
                        type="number" 
                        class="form-control form-control-sm set-reps" 
                        value="1" 
                        min="1">
                </td>
                <td class="text-center">
                    <button type="button" class="btn btn-danger btn-sm remove-set">Eliminar</button>
                </td>
            `;
            setTable.appendChild(newRow);

            // Agregar evento para eliminar
            newRow.querySelector(".remove-set").addEventListener("click", () => {
                const setId = newRow.getAttribute("data-set-id");
                if (setId) {
                    deletedSets.add(setId); // Marcar el ID como eliminado si ya existía
                }
                newRow.remove(); // Eliminar la fila del DOM
                updateSetNumbers(setTable); // Recalcular los números de las series
                removeExerciseIfEmpty(button.closest(".exercise-item")); // Verificar si el ejercicio debe eliminarse
            });

            updateSetNumbers(setTable); // Recalcular los números de las series
        });
    });

    // Manejar la eliminación de las series existentes
    document.querySelectorAll(".remove-set").forEach(button => {
        button.addEventListener("click", (event) => {
            const setRow = event.target.closest("tr");
            const setId = setRow.getAttribute("data-set-id");

            if (setId) {
                deletedSets.add(setId); // Marcar el ID como eliminado
            }

            setRow.remove(); // Eliminar la fila del DOM
            const setTable = button.closest("tbody");
            updateSetNumbers(setTable); // Recalcular los números de las series
            removeExerciseIfEmpty(button.closest(".exercise-item")); // Verificar si el ejercicio debe eliminarse
        });
    });

    // Cambiar la unidad de peso dinámicamente
    document.querySelectorAll(".weight-unit-selector").forEach(selector => {
        selector.addEventListener("change", (event) => {
            const exerciseItem = event.target.closest(".exercise-item");
            const unit = event.target.value; // kg o lb
            const weights = exerciseItem.querySelectorAll(".set-weight");

            weights.forEach(weightInput => {
                let weight = parseFloat(weightInput.value) || 0;

                if (unit === "kg") {
                    // Convertir de libras a kilogramos
                    weightInput.value = (weight / 2.20462).toFixed(1);
                } else if (unit === "lb") {
                    // Convertir de kilogramos a libras
                    weightInput.value = (weight * 2.20462).toFixed(1);
                }
            });
        });
    });

    // Guardar cambios
    const saveButton = document.querySelector(".save-changes");
    saveButton.addEventListener("click", async () => {
        const exercises = [];
        const workoutId = document.querySelector(".exercise-list").getAttribute("data-workout-id"); // Obtener el ID de la rutina

        if (!workoutId) {
            alert("Error: No se encontró el ID de la rutina.");
            return;
        }

        document.querySelectorAll(".exercise-item").forEach(exercise => {
            const exerciseId = exercise.getAttribute("data-exercise-id");
            const weightUnit = exercise.querySelector(".weight-unit-selector").value;
            const restTime = exercise.querySelector(".rest-time").value;

            const sets = Array.from(exercise.querySelectorAll(".set-item")).map(set => ({
                id: set.getAttribute("data-set-id"),
                set_number: set.getAttribute("data-set-number"),
                weight: set.querySelector(".set-weight").value,
                reps: set.querySelector(".set-reps").value,
            }));

            exercises.push({
                exercise_id: exerciseId,
                weight_unit: weightUnit,
                rest_time: restTime,
                sets,
            });
        });

        try {
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');

            const response = await fetch("/update_exercises/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": csrfToken,
                },
                body: JSON.stringify({ workout_id: workoutId, exercises, deleted_sets: Array.from(deletedSets) }),
            });

            if (response.ok) {
                alert("Cambios guardados exitosamente");
                location.reload(); // Recargar para reflejar los cambios
            } else {
                const errorData = await response.json();
                alert(`Error al guardar los cambios: ${errorData.error}`);
                console.error("Error del servidor:", errorData);
            }
        } catch (error) {
            console.error("Error en la solicitud:", error);
            alert("Hubo un error al guardar los cambios.");
        }
    });
});
