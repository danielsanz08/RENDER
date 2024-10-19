function validateForm() {
    const nombre = document.getElementById("nombre").value.trim();
    const cantidad = document.getElementById("cantidad").value;

    let errorMessages = [];

    const nombreRegex = /^[a-zA-Z\s]+$/;
    if (!nombreRegex.test(nombre)) {
        errorMessages.push('El nombre solo puede contener letras y espacios.');
    }

    if (cantidad < 0 || isNaN(cantidad)) {
        errorMessages.push('No se pueden ingresar números negativos.');
    }

    return errorMessages;
}

function checkIfInsumoExists(nombre) {
    return $.ajax({
        url: '/verificar_nombre_insumo/', // Asegúrate de que esta URL sea la correcta
        type: 'GET',
        data: { 'nombre': nombre },
        dataType: 'json'
    });
}

document.getElementById("add-insumo-form").addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío inmediato del formulario

    const nombre = document.getElementById("nombre").value.trim();

    checkIfInsumoExists(nombre).done(function(response) {
        let errorMessages = [];

        if (response.exists) {
            errorMessages.push('Ya existe un insumo con este nombre.');
        }

        // Acumula los errores de la validación del formulario
        const formErrors = validateForm();
        if (formErrors.length > 0) {
            errorMessages = errorMessages.concat(formErrors);
        }

        if (errorMessages.length > 0) {
            // Muestra todos los mensajes de error acumulados
            toastr.error(errorMessages.join('<br>'), 'Error', {
                closeButton: true,
                progressBar: true,
                timeOut: 5000,
                positionClass: 'toast-bottom-right'
            });
        } else {
            // Si no hay errores, muestra el mensaje de éxito y envía el formulario
            toastr.success('El insumo se ha agregado correctamente.', 'Éxito', {
                closeButton: true,
                progressBar: true,
                timeOut: 5000,
                positionClass: 'toast-bottom-right'
            });

            // Envía el formulario después del retraso
            setTimeout(function() {
                document.getElementById("add-insumo-form").submit();
            }, 2000); // Retrasa el envío 2 segundos
        }
    }).fail(function() {
        // Maneja errores en la solicitud AJAX si ocurren
        toastr.error('Ocurrió un error al verificar el nombre del insumo.', 'Error', {
            closeButton: true,
            progressBar: true,
            timeOut: 5000,
            positionClass: 'toast-bottom-right'
        });
    });
});
