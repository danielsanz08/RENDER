$(document).ready(function() {
    $('#editar-cliente-form').on('submit', function(event) {
        event.preventDefault(); // Evita el envío inmediato del formulario

        let errorMessages = [];
        const tipoCliente = $('select[name="tipo_cliente"]').val().trim();
        const nombre = $('input[name="nombre"]').val().trim();
        const email = $('input[name="email"]').val().trim();
        const telefono = $('input[name="telefono"]').val().trim();
        const direccion = $('input[name="direccion"]').val().trim();

        // Validaciones del formulario
        if (!tipoCliente) {
            errorMessages.push('Debe seleccionar un tipo de cliente.');
        }

        const nombreRegex = /^[a-zA-Z\s]+$/;
        if (nombre && !nombreRegex.test(nombre)) {
            errorMessages.push('El nombre solo puede contener letras y espacios.');
        }

        if (nombre && (nombre.length < 2 || nombre.length > 50)) {
            errorMessages.push('El nombre debe tener entre 2 y 50 caracteres.');
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (email && !emailRegex.test(email)) {
            errorMessages.push('Por favor, ingresa un correo electrónico válido.');
        }

        const telefonoRegex = /^\d{10}$/; 
        if (telefono && !telefonoRegex.test(telefono)) {
            errorMessages.push('El teléfono debe tener 10 dígitos.');
        }

        if (direccion && direccion.length < 5) {
            errorMessages.push('La dirección debe tener al menos 5 caracteres.');
        }

        // Si hay errores de validación, mostrar todos los mensajes
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
        }

        // Si no hay errores de validación, procedemos a verificar si el cliente ya existe solo si se cambian ciertos campos
        $.ajax({
            url: '/verificar_cliente/',  // Asegúrate de que esta URL esté definida en tus urls.py
            type: 'POST',
            data: {
                'nombre': nombre,
                'email': email,
                'telefono': telefono,
                'direccion': direccion,
                'tipo_cliente': tipoCliente,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()  // CSRF token
            },
            success: function(response) {
                if (response.exists) {
                    toastr.error('Este cliente ya existe.', 'Error', {
                        closeButton: true,
                        progressBar: true,
                        timeOut: 5000,
                        positionClass: 'toast-bottom-right'
                    });

                    // Ajustar la posición del toast
                    setTimeout(() => {
                        $('.toast').css('top', '-50px'); // Ajusta el valor a la posición deseada
                    }, 0);
                } else {
                    // Si no existe un cliente, mostramos el popup de éxito y enviamos el formulario
                    $('#popup').fadeIn(); // Muestra el popup

                    setTimeout(function() {
                        $('html, body').animate({
                            scrollTop: $('#popup').offset().top - 300 // Ajuste para que el popup quede más arriba
                        }, 300); // Desplazamiento suave hacia el popup

                        // Oculta el popup después de 2 segundos y envía el formulario
                        setTimeout(() => {
                            $('#popup').fadeOut(); // Oculta el popup
                            $('#editar-cliente-form')[0].submit(); // Envía el formulario
                        }, 2000); // Tiempo que el popup se muestra (2 segundos)
                    });
                }
            },
            error: function() {
                toastr.error('Error al verificar el registro.', 'Error', {
                    closeButton: true,
                    progressBar: true,
                    timeOut: 5000,
                    positionClass: 'toast-bottom-right'
                });
            }
        });
    });
});
$(document).ready(function() {
    $('#editar-cliente-form').on('submit', function(e) {
        var nombre = $('#nombre').val(); // Cambia el selector si es necesario
        var telefono = $('#telefono').val();
        var errorMessage = '';

        // Verificar si el nombre contiene números
        if (/\d/.test(nombre)) {
            errorMessage += 'El nombre no debe contener números.<br>';
        }

        // Verificar si el teléfono contiene letras
        if (/[a-zA-Z]/.test(telefono)) {
            errorMessage += 'El teléfono no debe contener letras.';
        }

        // Si hay errores, mostrar el mensaje de error
        if (errorMessage) {
            e.preventDefault(); // Previene el envío del formulario
            $('#popup').hide(); // Oculta el popup si estaba visible
            $('#error-message').html(errorMessage).show();
        } else {
            $('#error-message').hide(); // Oculta el mensaje de error si no hay errores
        }
    });

    // Ocultar el mensaje de error al escribir
    $('input[name="nombre"], input[name="telefono"]').on('input', function() {
        $('#error-message').hide();
    });
});