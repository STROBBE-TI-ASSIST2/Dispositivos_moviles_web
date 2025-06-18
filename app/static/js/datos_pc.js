// FUNCION PARA COLOCAR LOS DATOS EN EL FORMULARIO PARA LA ACTUALIZACION
document.addEventListener('DOMContentLoaded', async () => {
  const form = document.getElementById('formulario-mantenimiento');
  const modo = form?.dataset.modo;
  const id = form?.dataset.id;

  if (modo === 'editar' && id) {
    // Cargar datos desde el backend
    try {
      const res = await fetch(`/api/mantenimientos/${id}`);
      const data = await res.json();

      document.getElementById('codigo_stb').value = data.codigo_stb;
      document.getElementById('nombre_equipo').value = data.nombre_equipo;
      document.getElementById('ip').value = data.ip;
      document.getElementById('sistema_operativo').value = data.sistema_operativo;
      document.getElementById('procesador').value = data.procesador;
      document.getElementById('ram').value = data.ram;
      document.getElementById('office').value = data.office;
      document.getElementById('reporte').value = data.reporte || '';
      document.getElementById('accion').value = data.accion_correctiva || '';

      // Desactivar campos fijos
      ['codigo_stb', 'nombre_equipo', 'ip', 'sistema_operativo', 'procesador', 'ram', 'office'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.disabled = true;
      });

      // Ocultar lector QR
      const qrContainer = document.getElementById('contenedor-qr');
      if (qrContainer) qrContainer.style.display = 'none';

    } catch (err) {
      console.error('Error al cargar el mantenimiento:', err);
    }
  } else {
    // Renderizar QR solo en modo nuevo
    const qrScanner = new Html5QrcodeScanner("reader", { fps: 10, qrbox: 250 });
    qrScanner.render(onScanSuccess);
  }
});

// Función para capturar datos del QR
function onScanSuccess(decodedText) {
  const lineas = decodedText.trim().split('\n');
  const datos = {};
  lineas.forEach(linea => {
    const [clave, valor] = linea.split(':');
    if (clave && valor) datos[clave.trim().toLowerCase()] = valor.trim();
  });

  document.getElementById('codigo_stb').value = datos['codigo stb'];
  document.getElementById('nombre_equipo').value = datos['nombre de equipo'] || '';
  document.getElementById('ip').value = datos['ip'] || '';
  document.getElementById('sistema_operativo').value = datos['sistema operativo'] || '';
  document.getElementById('procesador').value = datos['procesador'] || '';
  document.getElementById('ram').value = datos['memoria ram'] || '';
  document.getElementById('office').value = datos['office'] || '';
}

// FUNCION PARA COLOCAR LOS DATOS EN EL FORMULARIO OBTENIDOS DEL QR
function recolectarDatos() {
  return {
    codigo_stb: document.getElementById('codigo_stb').value,
    nombre_equipo: document.getElementById('nombre_equipo').value,
    ip: document.getElementById('ip').value,
    sistema_operativo: document.getElementById('sistema_operativo').value,
    procesador: document.getElementById('procesador').value,
    ram: document.getElementById('ram').value,
    office: document.getElementById('office').value,
    reporte: document.getElementById('reporte')?.value,
    accion_correctiva: document.getElementById('accion')?.value
  };
}

// FUNCION PARA ENVIAR DATOS AL BACKEND (SEGUN SEA PARA GUARDAR O PARA ACTUALIZAR)
async function enviarDatos() {
  const form = document.getElementById('formulario-mantenimiento');
  const modo = form.dataset.modo;

  if (modo === 'editar') {
    await actualizarExistente(form);
  } else {
    await guardarNuevo(form);
  }
}

// FUNCION PARA GUARDAR MANTENIMIENTO
async function guardarNuevo(form) {
  const equipo_mante = recolectarDatos();

  try {
    const response = await fetch('/formulario', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(equipo_mante)
    });

    const data = await response.json();
    document.getElementById('respuesta').innerText = data.message || 'Guardado correctamente';

    if (response.ok) {
      limpiarFormulario();
    }
  } catch (error) {
    console.error(error);
    document.getElementById('respuesta').innerText = 'Error al guardar los datos.';
  }
}

// FUNCION PARA ACTUALIZAR MANTENIMIENTO
async function actualizarExistente(form) {
  const id = form.dataset.id;
  const equipo_mante = recolectarDatos();

  try {
    const response = await fetch(`/api/mantenimientos/actualizar/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(equipo_mante)
    });

    const data = await response.json();
    document.getElementById('respuesta').innerText = data.message || 'Actualizado correctamente';
  } catch (error) {
    console.error(error);
    document.getElementById('respuesta').innerText = 'Error al actualizar los datos.';
  }
}

// ELIMINAR REGISTRO
async function eliminarMantenimiento(id) {
  const confirmacion = confirm('¿Estás seguro de que deseas eliminar este mantenimiento?');
  if (!confirmacion) return;

  try {
    const res = await fetch(`/api/mantenimientos/${id}`, {
      method: 'DELETE'
    });

    const data = await res.json();
    alert(data.message);

    // Opcional: recargar página o eliminar visualmente la tarjeta
    location.reload();
  } catch (error) {
    console.error('Error al eliminar mantenimiento:', error);
    alert('Ocurrió un error al intentar eliminar el registro.');
  }
}

// FUNCION PARA LIMPIAR CAMPOS SI SE APLICA LA GUARDAR DATOS
function limpiarFormulario() {
  ['codigo_stb', 'nombre_equipo', 'ip', 'sistema_operativo', 'procesador', 'ram', 'office', 'reporte', 'accion']
    .forEach(id => {
      const el = document.getElementById(id);
      if (el) el.value = '';
    });

  const canvas = document.getElementById('qr-canvas-visible');
  if (canvas) canvas.getContext('2d').clearRect(0, 0, canvas.width, canvas.height);
}
