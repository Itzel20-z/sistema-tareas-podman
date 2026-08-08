// Ajusta esta URL si el backend corre en otro host/puerto.
// Cuando ambos contenedores corren en la misma máquina, el navegador
// llama al backend expuesto en localhost:5000 (mapeado desde Podman).
const API_URL = "http://localhost:5000/api/tareas";

const form = document.getElementById("tarea-form");
const tareaIdInput = document.getElementById("tarea-id");
const tituloInput = document.getElementById("titulo");
const descripcionInput = document.getElementById("descripcion");
const estadoInput = document.getElementById("estado");
const prioridadInput = document.getElementById("prioridad");
const fechaLimiteInput = document.getElementById("fecha_limite");
const tareasBody = document.getElementById("tareas-body");
const mensajeDiv = document.getElementById("mensaje");
const btnCancelar = document.getElementById("btn-cancelar");
const formTitulo = document.getElementById("form-titulo");
const filtroEstado = document.getElementById("filtro-estado");

function mostrarMensaje(texto, tipo = "ok") {
  mensajeDiv.textContent = texto;
  mensajeDiv.className = `mensaje ${tipo}`;
  setTimeout(() => { mensajeDiv.textContent = ""; }, 3000);
}

function limpiarFormulario() {
  form.reset();
  tareaIdInput.value = "";
  formTitulo.textContent = "Nueva tarea";
  btnCancelar.style.display = "none";
}

async function cargarTareas() {
  try {
    const estado = filtroEstado.value;
    const url = estado ? `${API_URL}?estado=${estado}` : API_URL;
    const resp = await fetch(url);
    if (!resp.ok) throw new Error("Error al obtener tareas");
    const tareas = await resp.json();
    renderizarTareas(tareas);
  } catch (err) {
    mostrarMensaje("No se pudo conectar con la API: " + err.message, "error");
  }
}

function renderizarTareas(tareas) {
  tareasBody.innerHTML = "";
  if (tareas.length === 0) {
    tareasBody.innerHTML = `<tr><td colspan="5">No hay tareas registradas.</td></tr>`;
    return;
  }
  tareas.forEach((t) => {
    const fila = document.createElement("tr");
    fila.innerHTML = `
      <td>${escapeHtml(t.titulo)}</td>
      <td><span class="badge badge-${t.estado}">${t.estado.replace("_", " ")}</span></td>
      <td>${t.prioridad}</td>
      <td>${t.fecha_limite || "-"}</td>
      <td>
        <button class="accion-btn" onclick="editarTarea(${t.id})">Editar</button>
        <button class="accion-btn eliminar" onclick="eliminarTarea(${t.id})">Eliminar</button>
      </td>
    `;
    tareasBody.appendChild(fila);
  });
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();

  const payload = {
    titulo: tituloInput.value.trim(),
    descripcion: descripcionInput.value.trim(),
    estado: estadoInput.value,
    prioridad: prioridadInput.value,
    fecha_limite: fechaLimiteInput.value || null,
  };

  const idExistente = tareaIdInput.value;

  try {
    let resp;
    if (idExistente) {
      resp = await fetch(`${API_URL}/${idExistente}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    } else {
      resp = await fetch(API_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });
    }

    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || "Error al guardar");

    mostrarMensaje(idExistente ? "Tarea actualizada" : "Tarea creada", "ok");
    limpiarFormulario();
    cargarTareas();
  } catch (err) {
    mostrarMensaje(err.message, "error");
  }
});

async function editarTarea(id) {
  try {
    const resp = await fetch(`${API_URL}/${id}`);
    if (!resp.ok) throw new Error("No se encontró la tarea");
    const t = await resp.json();

    tareaIdInput.value = t.id;
    tituloInput.value = t.titulo;
    descripcionInput.value = t.descripcion || "";
    estadoInput.value = t.estado;
    prioridadInput.value = t.prioridad;
    fechaLimiteInput.value = t.fecha_limite || "";

    formTitulo.textContent = `Editando tarea #${t.id}`;
    btnCancelar.style.display = "inline-block";
    window.scrollTo({ top: 0, behavior: "smooth" });
  } catch (err) {
    mostrarMensaje(err.message, "error");
  }
}

async function eliminarTarea(id) {
  if (!confirm("¿Seguro que deseas eliminar esta tarea?")) return;
  try {
    const resp = await fetch(`${API_URL}/${id}`, { method: "DELETE" });
    const data = await resp.json();
    if (!resp.ok) throw new Error(data.error || "Error al eliminar");
    mostrarMensaje("Tarea eliminada", "ok");
    cargarTareas();
  } catch (err) {
    mostrarMensaje(err.message, "error");
  }
}

btnCancelar.addEventListener("click", limpiarFormulario);
filtroEstado.addEventListener("change", cargarTareas);

// Carga inicial
cargarTareas();
