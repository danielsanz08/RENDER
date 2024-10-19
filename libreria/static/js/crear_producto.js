$(document).ready(function() {
    $('#productoForm').on('submit', function(event) {
        event.preventDefault(); // Evita el envío inmediato del formulario

        let errorMessages = [];
        const nombre = $('#nombre').val().trim();
        const categoria = $('#categoria').val();
        const presentacion = $('#presentacion').val().trim();
        const unidadMedida = $('#unidad_medida').val();
        const cantidad = $('#cantidad').val();
        const precio = $('#precio').val();
        const fechaElaboracion = $('#fecha_elaboracion').val();
        const fechaVencimiento = $('#fecha_vencimiento').val();
        const temperaturaConservacion = $('#temperatura_conservacion').val();
        const lote = $('#lote').val().trim();
        const codigo = $('#codigo').val().trim();

        // Validaciones...
        const nombreRegex = /^[A-Za-zÁáÉéÍíÓóÚúÑñ\s]+$/;
        const numericRegex = /^[0-9]+$/;

        if (!nombreRegex.test(nombre)) {
            errorMessages.push('El nombre solo puede contener letras y espacios.');
        }

        if (categoria === "") {
            errorMessages.push('Debes seleccionar una categoría.');
        }

        // Validación de presentación: Solo letras y espacios, y entre 3 y 100 caracteres
        if (!nombreRegex.test(presentacion)) {
            errorMessages.push('La presentación solo puede contener letras y espacios.');
        } else if (presentacion.length < 3 || presentacion.length > 10) {
            errorMessages.push('La presentación debe tener entre 3 y 10 caracteres.');
        }

        if (unidadMedida === "") {
            errorMessages.push('Debes seleccionar una unidad de medida.');
        }

        if (cantidad <= 0) {
            errorMessages.push('La cantidad debe ser mayor a 0.');
        }

        if (precio <= 0) {
            errorMessages.push('El precio debe ser mayor a 0.');
        }

        if (fechaElaboracion > fechaVencimiento) {
            errorMessages.push('La fecha de elaboración no puede ser posterior a la fecha de vencimiento.');
        }

        if (temperaturaConservacion < -20 || temperaturaConservacion > 30) {
            errorMessages.push('La temperatura de conservación debe estar entre -20 y 30 °C.');
        }

        if (!numericRegex.test(lote)) {
            errorMessages.push('El lote debe contener solo números.');
        }

        if (!numericRegex.test(codigo)) {
            errorMessages.push('El código debe contener solo números.');
        }

        // Si hay errores de validación, mostrar mensajes de error
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

        // Si no hay errores, mostrar el popup y desplazar hacia él
        $('#popup').fadeIn(); // Muestra el popup

        setTimeout(function() {
            $('html, body').animate({
                scrollTop: $('#popup').offset().top - 300 // Ajuste para que el popup quede más arriba
            }, 300); // Desplazamiento suave hacia el popup

            setTimeout(() => {
                $('#popup').fadeOut(); // Oculta el popup después de 2 segundos
                // Enviar el formulario después de que el popup se oculta
                $('#productoForm')[0].submit(); 
            }, 2000); // Tiempo que el popup se muestra (2 segundos)
        });
    });
});
