function validateUpdateForm() {
    const nombre = document.getElementById("id_nombre").value.trim(); // Asegúrate de que el id sea el correcto
    const cantidad = document.getElementById("id_cantidad").value;
    const originalNombre = document.getElementById("original-nombre").value; // Nombre original del insumo

    // Reinicia los mensajes de error
    toastr.clear();

    let errorMessages = []; // Acumula los mensajes de error

    // Validación del nombre
    const nombreRegex = /^[a-zA-Z\s]+$/;
    if (!nombreRegex.test(nombre)) {
        errorMessages.push('El nombre solo puede contener letras y espacios.');
    }

    // Validación de la cantidad
    if (cantidad < 0 || isNaN(cantidad)) {
        errorMessages.push('No se pueden ingresar números negativos.');
    }

    // Verifica si el nombre ya existe en la base de datos
    $.ajax({
        url: '/verificar_nombre_insumo/', // URL de tu endpoint de verificación
        type: 'GET',
        data: { 'nombre': nombre },
        dataType: 'json',
        success: function(response) {
            if (response.exists && nombre !== originalNombre) {
                errorMessages.push('Ya existe un insumo con este nombre.');
            }

            // Muestra todos los mensajes de error acumulados (locales y de la verificación AJAX)
            if (errorMessages.length > 0) {
                toastr.error(errorMessages.join('<br>'), 'Error', {
                    closeButton: true,
                    progressBar: true,
                    timeOut: 5000,
                    positionClass: 'toast-bottom-right'
                });
            } else {
                // Si no hay errores, muestra el mensaje de éxito y envía el formulario
                toastr.success('El insumo se ha modificado correctamente.', 'Éxito', {
                    closeButton: true,
                    progressBar: true,
                    timeOut: 5000,
                    positionClass: 'toast-bottom-right'
                });

                // Envía el formulario después del retraso
                setTimeout(function() {
                    document.getElementById("update-insumo-form").submit();
                }, 2000); // Retrasa el envío 2 segundos
            }
        },
        error: function() {
            toastr.error('Ocurrió un error al verificar el nombre del insumo.', 'Error', {
                closeButton: true,
                progressBar: true,
                timeOut: 5000,
                positionClass: 'toast-bottom-right'
            });
        }
    });

    return false; // Previene el envío inmediato del formulario
}

// Asocia la función de validación al evento submit del formulario
document.getElementById("update-insumo-form").addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío inmediato del formulario
    validateUpdateForm(); // Ejecuta la validación
});
