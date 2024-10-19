let productoIdToDelete = null; // Variable global para almacenar el ID del producto a eliminar

function showConfirmModal(event, productoId, productoNombre) {
    event.preventDefault(); // Evita que se siga el enlace

    // Establece el ID y el nombre del producto en el modal
    productoIdToDelete = productoId;
    document.getElementById('producto-nombre').textContent = productoNombre;

    // Configura la acción del formulario de eliminación
    const deleteForm = document.getElementById('delete-form-producto');
    deleteForm.action = `/productos/eliminar/${productoIdToDelete}/`; // Asegúrate de que esta URL sea correcta

    // Muestra el modal y el overlay
    document.getElementById('eliminar_producto').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';

    // Desvanecer elementos de la pantalla
    fadeOutElements();
}

function cerrarVentana() {
    // Oculta el modal y el overlay
    document.getElementById('eliminar_producto').style.display = 'none';
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

// Agregar evento para cerrar el modal al hacer clic en el overlay
document.getElementById('overlay').addEventListener('click', cerrarVentana);

// Para asegurar que el modal se cierre al presionar la tecla ESC
document.addEventListener('keydown', function(event) {
    if (event.key === "Escape") {
        cerrarVentana();
    }
});
