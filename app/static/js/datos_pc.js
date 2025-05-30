
  function onScanSuccess(decodedText, decodedResult) {
    console.log("Texto completo del QR:", decodedText);

    // Separar por líneas
    const lineas = decodedText.trim().split('\n');
    console.log("Líneas:", lineas);

    // Crear un objeto clave:valor
    const datos = {};
    lineas.forEach(linea => {
      const [clave, valor] = linea.split(':');
      if (clave && valor) {
        datos[clave.trim().toLowerCase()] = valor.trim();
      }
    });

    // Asignar los valores a los campos correspondientes
    document.getElementById('codigo_stb').value = datos['codigo stb'];
    document.getElementById('nombre_equipo').value = datos['nombre de equipo'] || '';
    document.getElementById('ip').value = datos['ip'] || '';
    document.getElementById('sistema_operativo').value = datos['sistema operativo'] || '';
    document.getElementById('procesador').value = datos['procesador'] || '';
    document.getElementById('ram').value = datos['memoria ram'] || '';
    document.getElementById('office').value = datos['office'] || '';

    //html5QrcodeScanner.clear(); // Detener escaneo
  }

  var html5QrcodeScanner = new Html5QrcodeScanner(
    "reader", { fps: 10, qrbox: 250 });
  html5QrcodeScanner.render(onScanSuccess);

async function enviarDatos() {
  const equipo_mante = {
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

  try {
    const response = await fetch('/formulario', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(equipo_mante)
    });

    const data = await response.json();

    if (response.ok) {
      document.getElementById('respuesta').innerText = data.message || 'Datos guardados correctamente.';

      // Limpiar campos del formulario
      const formElements = ['codigo_stb', 'nombre_equipo', 'ip', 'sistema_operativo', 'procesador', 'ram', 'office', 'reporte', 'accion'];
      formElements.forEach(id => {
        const el = document.getElementById(id);
        if (el) el.value = '';
      });

      // Limpiar el canvas del escáner
      const canvas = document.getElementById('qr-canvas-visible');
      if (canvas) {
        const ctx = canvas.getContext('2d');
        ctx.clearRect(0, 0, canvas.width, canvas.height);
      }
    } else {
      document.getElementById('respuesta').innerText = data.message || 'Error desconocido al guardar.';
    }
  } catch (error) {
    console.error(error);
    document.getElementById('respuesta').innerText = 'Error al enviar los datos.';
  }
}


