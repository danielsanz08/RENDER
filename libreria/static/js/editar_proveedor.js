$(document).ready(function() {
    $('#form-editar').on('submit', function(event) {
        event.preventDefault(); // Evita el envío inmediato del formulario

        let errorMessages = [];
        const nit = $('#id_nit').val().trim();
        const nombre = $('#id_nombre').val().trim();
        const direccion = $('#id_direccion').val().trim();
        const email = $('#id_email').val().trim();
        const telefono = $('#id_telefono').val().trim();

        // Validaciones...
        const nitRegex = /^\d{9,11}-\d{1}$/; // Permite de 9 a 11 números, un guion y un dígito
        if (!nitRegex.test(nit)) {
            errorMessages.push('El NIT debe tener de 9 a 11 números, seguido de un guion y un dígito.');
        }

        const nombreRegex = /^[a-zA-Z\s]+$/;
        if (nombre && !nombreRegex.test(nombre)) {
            errorMessages.push('El nombre solo puede contener letras y espacios.');
        }

        if (direccion && direccion.length < 5) {
            errorMessages.push('La dirección debe tener al menos 5 caracteres.');
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (email && !emailRegex.test(email)) {
            errorMessages.push('Por favor, ingresa un correo electrónico válido.');
        }

        const telefonoRegex = /^\d{10}$/;
        if (telefono && !telefonoRegex.test(telefono)) {
            errorMessages.push('El teléfono debe tener 10 dígitos.');
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
                $('.toast').css('top', '-50px');
            }, 0);
            return;
        }

        // Si no hay errores, mostrar el popup y enviar el formulario
        $('#popup').fadeIn(); // Muestra el popup

        setTimeout(function() {
            $('html, body').animate({
                scrollTop: $('#popup').offset().top - 300 // Ajuste para que el popup quede más arriba
            }, 300); // Desplazamiento suave hacia el popup

            setTimeout(() => {
                $('#popup').fadeOut(); // Oculta el popup después de 2 segundos
                $('#form-editar')[0].submit(); // Envía el formulario
            }, 2000); // Tiempo que el popup se muestra (2 segundos)
        });
    });
});
