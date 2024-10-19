function showConfirmModal(proveedorId, proveedorNombre) {
    // Configura el nombre del proveedor en el modal
    document.getElementById('proveedor-nombre').textContent = proveedorNombre;

    // Configura la acción del formulario de eliminación
    const deleteForm = document.getElementById('delete-form');
    deleteForm.action = `/proveedores/eliminar/${proveedorId}/`; // Cambia esta ruta según tu URL

    // Muestra el modal y el overlay
    document.getElementById('eliminar_proveedor').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';

    // Desvanecer elementos adicionales
    fadeOutElements();
}

function cerrarVentana() {
    // Oculta el modal y el overlay
    document.getElementById('eliminar_proveedor').style.display = 'none';
    document.getElementById('overlay').style.display = 'none';

    // Mostrar nuevamente los elementos quitando la clase de desvanecimiento
    resetFadeOutElements();
}

function confirmDelete() {
    // Aquí el formulario de eliminación se envía cuando se confirma la eliminación
    document.getElementById('delete-form').submit();
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

// Agregar evento para cerrar el modal al hacer clic en el overlay
document.getElementById('overlay').addEventListener('click', cerrarVentana);

// Para asegurar que el modal se cierre al presionar la tecla ESC
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        cerrarVentana();
    }
});