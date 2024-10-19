let insumoIdToDelete = null; // Variable global para almacenar el ID del insumo a eliminar

function showConfirmModal(event, insumoId, insumoNombre) {
    event.preventDefault(); // Evita que se siga el enlace

    // Establece el ID y el nombre del insumo en el modal
    insumoIdToDelete = insumoId;
    document.getElementById('insumo-nombre').textContent = insumoNombre;

    // Configura la acción del formulario de eliminación
    const deleteForm = document.getElementById('delete-insumo-form');
    deleteForm.action = `/insumos/eliminar/${insumoIdToDelete}/`; // Asegúrate de que esta URL sea correcta

    // Muestra el modal y el overlay
    document.getElementById('eliminar_insumo').style.display = 'block';
    document.getElementById('overlay').style.display = 'block';

    // Desvanecer elementos de la pantalla
    fadeOutElements();
}

function confirmDelete() {
    const form = document.getElementById('delete-insumo-form');
    form.submit(); // Envía el formulario para eliminar el insumo
}

function cerrarVentana() {
    // Oculta el modal y el overlay
    document.getElementById('eliminar_insumo').style.display = 'none';
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
