function ensureAlertContainer() {
    let container = document.getElementById("alert-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "alert-container";
        container.classList.add("alert-container");

        const mainContainer = document.getElementById("main-container");
        if (mainContainer) {
            mainContainer.prepend(container);
        } else {
            document.body.prepend(container);
        }
    }
    return container;
}

function showBootstrapAlert(message, type = "danger") {
    const alertContainer = ensureAlertContainer();
    if (!alertContainer) return;

    alertContainer.innerHTML = "";

    const alertDiv = document.createElement("div");
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.setAttribute("role", "alert");

    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
    `;
    alertContainer.appendChild(alertDiv);
}

document.addEventListener("DOMContentLoaded", () => {
    const deletedSets = new Set();
  
    function updateSetNumbers(table) {
      const rows = table.querySelectorAll("tr.set-item");
      rows.forEach((row, index) => {
        const setNumber = index + 1;
        row.querySelector(".set-number").textContent = setNumber;
        row.setAttribute("data-set-number", setNumber);
      });
    }
  
    function removeExerciseIfEmpty(exerciseEl) {
      const sets = exerciseEl.querySelectorAll(".set-item");
      if (sets.length === 0) {
        exerciseEl.classList.add("d-none");
      }
    }
  
    document.querySelectorAll(".add-set").forEach(button => {
      button.addEventListener("click", () => {
        const setTable = button.closest(".card-body")?.querySelector("tbody");
        if (!setTable) return;
  
        const newRow = document.createElement("tr");
        newRow.classList.add("set-item");
       
        newRow.innerHTML = `
            <td class="set-number"></td>
            <td>
                <input 
                    type="number"
                    class="form-control form-control-sm set-weight"
                    value="0"
                    step="0.1"
                >
            </td>
            <td>
                <input
                    type="number"
                    class="form-control form-control-sm set-reps"
                    value="0"
                    min="1"
                >
            </td>
            <td class="text-center">
                <button type="button" class="btn btn-danger btn-sm remove-set">Eliminar</button>
            </td>
        `;
        setTable.appendChild(newRow);
  
       
        newRow.querySelector(".remove-set").addEventListener("click", () => {
          const setId = newRow.getAttribute("data-set-id");
          if (setId) {
            deletedSets.add(setId);
          }
          newRow.remove();
         
          const updatedTable = setTable; 
          if (updatedTable) {
            updateSetNumbers(updatedTable);
          }
  
          const exerciseEl = button.closest(".exercise-item");
          removeExerciseIfEmpty(exerciseEl);
        });
  
        updateSetNumbers(setTable);
      });
    });
  
    document.querySelectorAll(".remove-set").forEach(button => {
      button.addEventListener("click", event => {
        const setRow = event.target.closest("tr.set-item");
        const setId = setRow.getAttribute("data-set-id");
        if (setId) {
          deletedSets.add(setId);
        }
  
        const exerciseEl = button.closest(".exercise-item");
        const setTable = exerciseEl.querySelector("tbody");
  
        setRow.remove();
  
        if (setTable) {
          updateSetNumbers(setTable);
        }
  
        removeExerciseIfEmpty(exerciseEl);
      });
    });
  
    document.querySelectorAll(".weight-unit-selector").forEach(selector => {
      selector.addEventListener("change", event => {
        const exerciseEl = event.target.closest(".exercise-item");
        const unit = event.target.value;
        const weightInputs = exerciseEl.querySelectorAll(".set-weight");
  
        weightInputs.forEach(weightInput => {
          let currentVal = parseFloat(weightInput.value) || 0;
          if (unit === "kg") {
            weightInput.value = (currentVal / 2.20462).toFixed(1);
          } else if (unit === "lb") {
            weightInput.value = (currentVal * 2.20462).toFixed(1);
          }
        });
      });
    });
  
    const saveButton = document.querySelector(".save-changes");
    if (saveButton) {
      saveButton.addEventListener("click", async () => {
        const exerciseListEl = document.querySelector(".exercise-list");
        if (!exerciseListEl) {
          showBootstrapAlert("Error: Exercise list not found", "danger");
          return;
        }
  
        const workoutId = exerciseListEl.getAttribute("data-workout-id");
        if (!workoutId) {
          showBootstrapAlert("Error: Workout ID not found", "danger");
          return;
        }
  
        const exercises = [];
        document.querySelectorAll(".exercise-item").forEach(exerciseEl => {
          const exerciseId = exerciseEl.getAttribute("data-exercise-id");
          const restTime = exerciseEl.querySelector(".rest-time")?.value || "00:00";
          const weightUnit = exerciseEl.querySelector(".weight-unit-selector")?.value || "kg";

          const sets = Array.from(exerciseEl.querySelectorAll(".set-item")).map(row => ({
            id: row.getAttribute("data-set-id") || null,
            set_number: row.getAttribute("data-set-number"),
            weight: row.querySelector(".set-weight").value,
            reps: row.querySelector(".set-reps").value
          }));
  
          exercises.push({
            exercise_id: exerciseId,
            weight_unit: weightUnit,
            rest_time: restTime,
            sets
          });
        });
  
        try {
          const csrfToken = document.querySelector('meta[name="csrf-token"]')?.getAttribute('content');
  
          const response = await fetch("/update_exercises/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": csrfToken
            },
            body: JSON.stringify({
              workout_id: workoutId,
              exercises,
              deleted_sets: Array.from(deletedSets)
            })
          });
  
          if (response.ok) {
            const data = await response.json();
            showBootstrapAlert(
              data.message || "Exercises and sets updated successfully",
              "success"
            );
  
            if (data.workout_removed) {
              window.location.href = data.redirect_url || "/workouts/";
              return;
            }
  
            if (data.exercises_removed && Array.isArray(data.exercises_removed)) {
              data.exercises_removed.forEach(exId => {
                const exEl = document.querySelector(`.exercise-item[data-exercise-id="${exId}"]`);
                if (exEl) {
                  exEl.remove(); 
                }
              });
            }
  
          } else {
            const errorData = await response.json();
            showBootstrapAlert(errorData.error || "Failed to save changes", "danger");
            console.error("Server error:", errorData);
          }
        } catch (error) {
          console.error("Request error:", error);
          showBootstrapAlert("An error occurred while saving", "danger");
        }
      });
    }
  });