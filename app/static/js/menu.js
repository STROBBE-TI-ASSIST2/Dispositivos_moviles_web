// Asume que tus íconos tienen un ID
document.addEventListener('DOMContentLoaded', () => {
  const callButton = document.getElementById('call-button');
  const whatsappButton = document.getElementById('whatsapp-button');

  // Número de teléfono para llamada
  const phoneNumber = '+51992495444'; // <-- Reemplaza con tu número

  // Número de WhatsApp (sin "+" y sin espacios)
  const whatsappNumber = '992495444'; // <-- Reemplaza con tu número

  if (callButton) {
    callButton.addEventListener('click', () => {
      window.location.href = `tel:${phoneNumber}`;
    });
  }

  if (whatsappButton) {
    whatsappButton.addEventListener('click', () => {
      window.open(`https://wa.me/${whatsappNumber}`, '_blank');
    });
  }
});

document.addEventListener('DOMContentLoaded', () => {
  const boton = document.getElementById('boton-formulario');
  boton.addEventListener('click', () => {
    window.location.href = "/formulario"; // o usa url_for en plantilla
  });
});
