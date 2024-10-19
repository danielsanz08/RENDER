function showConfirmModal(event, transaccionId, transaccionTipo) {
    event.preventDefault(); // Evita que el enlace se siga

    // Establece el tipo de transacción en el modal
    document.getElementById('transaccion-nombre').textContent = transaccionTipo;

    // Configura la acción del formulario de eliminación
    const deleteForm = document.getElementById('delete-form-transaccion');
    deleteForm.action = `/transacciones/eliminar/${transaccionId}/`; // Asegúrate de que esta URL sea correcta

    // Muestra el modal
    document.getElementById('confirmModal').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';

    // Desvanecer elementos de la pantalla
    fadeOutElements();
}

function closeModal() {
    // Oculta el modal y el overlay
    document.getElementById('confirmModal').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';

    // Mostrar nuevamente los elementos quitando la clase de desvanecimiento
    resetFadeOutElements();
}

function fadeOutElements() {
    const elementsToFade = [
        '#main-header',
        '.navbar',
        'footer',
        '#toggle-accessibility-menu'
    ];

    elementsToFade.forEach(selector => {
        const element = document.querySelector(selector);
        if (element) {
            element.classList.add('fade-out');
        }
    });
}

function resetFadeOutElements() {
    const elementsToReset = [
        '#main-header',
        '.navbar',
        'footer',
        '#toggle-accessibility-menu'
    ];

    elementsToReset.forEach(selector => {
        const element = document.querySelector(selector);
        if (element) {
            element.classList.remove('fade-out');
        }
    });
}

