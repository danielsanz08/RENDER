$(document).ready(function() {
    $('#edit-insumo-form').on('submit', function(event) {
        event.preventDefault(); // Evita el envío inmediato del formulario

        let errorMessages = [];
        const nombre = $('#id_nombre').val().trim();
        const presentacion = $('#id_presentacion').val().trim();
        const unidadMedida = $('#id_unidad_medida').val();
        const cantidad = $('#id_cantidad').val();
        const precio = $('#id_precio').val();
        const codigo = $('#id_codigo').val().trim();

        const nombreRegex = /^[A-Za-zÁáÉéÍíÓóÚúÑñ\s]+$/;
        const numericRegex = /^[0-9]+$/;

        // Validaciones...
        if (!nombreRegex.test(nombre)) {
            errorMessages.push('El nombre solo puede contener letras y espacios.');
        }

        if (!nombreRegex.test(presentacion) || presentacion.length < 3 || presentacion.length > 10) {
            errorMessages.push('La presentación debe tener entre 3 y 10 caracteres y solo puede contener letras y espacios.');
        }

        if (unidadMedida === "") {
            errorMessages.push('Debes seleccionar una unidad de medida.');
        }

        if (isNaN(cantidad) || cantidad <= 0) {
            errorMessages.push('La cantidad debe ser un número positivo.');
        }

        if (isNaN(precio) || precio <= 0) {
            errorMessages.push('El precio debe ser un número positivo.');
        }

        if (!numericRegex.test(codigo) || codigo.length < 4 || codigo.length > 8) {
            errorMessages.push('El código debe contener solo números y tener entre 4 y 8 dígitos.');
        }

        // Mostrar errores si existen
        if (errorMessages.length > 0) {
            toastr.error(errorMessages.join('<br>'), 'Error', {
                closeButton: true,
                progressBar: true,
                timeOut: 5000,
                positionClass: 'toast-bottom-right'
            });
            setTimeout(() => {
                $('.toast').css('top', '-50px'); // Ajusta el valor a la posición deseada
            }, 0);
            return; // Termina aquí si hay errores
        }

        // Mostrar el popup y luego enviar el formulario
        $('#popup').fadeIn();

        setTimeout(function() {
            $('#popup').fadeOut(); // Ocultar el popup después de 2 segundos
            $('#edit-insumo-form')[0].submit(); // Enviar el formulario
        }, 2000); // Tiempo que el popup se muestra (2 segundos)
    });
});
