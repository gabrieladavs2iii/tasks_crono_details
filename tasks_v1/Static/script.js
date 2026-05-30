console.log("script cargado correctamente");

function cargarTareas() {
  fetch("/api/tareas")
    .then(res => res.json())
    .then(rows => {
      const tbody = document.getElementById("tabla-tareas");
      tbody.innerHTML = "";
      let totalDias = 0;

      rows.forEach(r => {
        totalDias += r.dias;
        const tr = document.createElement("tr");

        const btn = document.createElement("button");
        btn.textContent = "🗑️";
        btn.addEventListener("click", () => eliminarTarea(r.id));

        tr.innerHTML = `
          <td>${r.responsable}</td>
          <td>${r.tarea}</td>
          <td>${r.dias}</td>
          <td>${r.porcentaje}%</td>
        `;
        const tdAcciones = document.createElement("td");
        tdAcciones.appendChild(btn);
        tr.appendChild(tdAcciones);

        tbody.appendChild(tr);
      });

      document.getElementById("total-dias").textContent = totalDias;
      document.getElementById("total-porcentaje").textContent = ((totalDias / 5) * 100).toFixed(0) + "%";
    });
}

function guardarTarea() {
  const responsable = document.getElementById("resp").value.trim();
  const tarea = document.getElementById("task").value.trim();
  const dias = document.getElementById("days").value;

  if (!responsable || !tarea || dias === "") {
    alert("Por favor completa todos los campos.");
    return;
  }

  fetch("/api/tareas", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({responsable, tarea, dias})
  })
  .then(res => res.json())
  .then(() => {
    document.getElementById("resp").value = "";
    document.getElementById("task").value = "";
    document.getElementById("days").value = "";
    cargarTareas();
  });
}

function eliminarTarea(id) {
  fetch("/api/tareas/" + id, { method: "DELETE" })
    .then(res => res.json())
    .then(() => cargarTareas());
}

// Asignar evento directamente
document.getElementById("btnAgregar").addEventListener("click", guardarTarea);

// Cargar tareas al inicio
cargarTareas();
