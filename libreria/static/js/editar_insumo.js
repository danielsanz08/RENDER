// Función para validar el formulario de edición de insumos
function validateForm() {
    const nombre = document.getElementById("id_nombre").value.trim();
    const cantidad = document.getElementById("id_cantidad").value;
    const descripcion = document.getElementById("id_descripcion").value.trim(); // Asegúrate de que el id sea correcto

    let errorMessages = [];

    // Validación del nombre: solo letras y espacios
    const nombreRegex = /^[a-zA-Z\s]+$/;
    if (!nombreRegex.test(nombre)) {
        errorMessages.push('El nombre solo puede contener letras y espacios.');
    }

    // Validación de la longitud de la descripción
    if (descripcion.length > 20) { 
        errorMessages.push('La descripción no puede contener más de 20 caracteres.');
    }

    // Validación de la cantidad: no puede ser negativa ni no numérica
    if (cantidad < 0 || isNaN(cantidad)) {
        errorMessages.push('No se pueden ingresar números negativos.');
    }

    return errorMessages;
}

// Función para verificar si el insumo ya existe en la base de datos
function checkIfInsumoExists(nombre) {
    return $.ajax({
        url: '/verificar_nombre_insumo/', // Asegúrate de que esta URL sea la correcta
        type: 'GET',
        data: { 'nombre': nombre },
        dataType: 'json'
    });
}

// Evento de envío del formulario de edición de insumos
document.getElementById("update-insumo-form").addEventListener('submit', function(event) {
    event.preventDefault(); // Evita el envío inmediato del formulario

    const nombre = document.getElementById("id_nombre").value.trim();
    const originalNombre = document.getElementById("original-nombre").value; // Nombre original del insumo

    // Realiza la verificación AJAX primero
    checkIfInsumoExists(nombre).done(function(response) {
        let errorMessages = [];

        // Verifica si ya existe el nombre y si ha sido modificado
        if (response.exists && nombre !== originalNombre) {
            errorMessages.push('Ya existe un insumo con este nombre.');
        }

        // Acumula los errores de la validación del formulario
        const formErrors = validateForm();
        if (formErrors.length > 0) {
            errorMessages = errorMessages.concat(formErrors);
        }

        // Muestra todos los mensajes de error acumulados si los hay
        if (errorMessages.length > 0) {
            toastr.error(errorMessages.join('<br>'), 'Error', {
                closeButton: true,
                progressBar: true,
                timeOut: 5000,
                positionClass: 'toast-bottom-right'
            });
            // Ajustar la posición del toast después de que se muestre
            setTimeout(() => {
                $('.toast').css('top', '-50px'); // Ajusta el valor a la posición deseada
            }, 0);
            return; // Termina aquí si hay errores
        } else {
            // Si no hay errores, muestra el popup y envía el formulario
            $('#popup').fadeIn(); // Muestra el popup

            setTimeout(function() {
                $('html, body').animate({
                    scrollTop: $('#popup').offset().top - 300 // Ajuste para que el popup quede más arriba
                }, 300); // Desplazamiento suave hacia el popup

                // Oculta el popup después de 2 segundos y envía el formulario
                setTimeout(() => {
                    $('#popup').fadeOut(); // Oculta el popup
                    document.getElementById("update-insumo-form").submit(); // Envía el formulario
                }, 2000); // Tiempo que el popup se muestra (2 segundos)
            });
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
