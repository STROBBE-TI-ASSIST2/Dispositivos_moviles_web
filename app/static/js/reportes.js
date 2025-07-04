document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("form-reporte");

  form.addEventListener("submit", (e) => {
    const checkboxes = form.querySelectorAll("input[name='columnas']:checked");

    if (checkboxes.length === 0) {
      e.preventDefault(); // Previene el envío
      alert("⚠️ Por favor selecciona al menos una columna para generar el reporte.");
    }
  });
});
