$(document).ready(function() {
    $('#crear-cliente-form').on('submit', function(event) {
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
        if (!nombreRegex.test(nombre)) {
            errorMessages.push('El nombre solo puede contener letras y espacios.');
        }

        if (nombre.length < 2 || nombre.length > 50) {
            errorMessages.push('El nombre debe tener entre 2 y 50 caracteres.');
        }

        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(email)) {
            errorMessages.push('Por favor, ingresa un correo electrónico válido.');
        }

        // Nueva validación para verificar que no se ingresen letras en el teléfono
        const telefonoRegex = /^\d{10}$/; 
        const letrasEnTelefono = /[a-zA-Z]/; // Expresión regular para detectar letras
        if (letrasEnTelefono.test(telefono)) {
            errorMessages.push('No se puede digitar letras en el teléfono.');
        } else if (!telefonoRegex.test(telefono)) {
            errorMessages.push('El teléfono debe tener 10 dígitos.');
        }

        if (direccion.length < 5) {
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

        // Si no hay errores de validación, procedemos a verificar si el cliente ya existe
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
                            $('#crear-cliente-form')[0].submit(); // Envía el formulario
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
    $('#numero_documento').on('input', function() {
        // Filtrar la entrada para que solo permita números
        this.value = this.value.replace(/[^0-9]/g, '');
        // Si se ingresan letras, mostrar un mensaje de error
        if (/[a-zA-Z]/.test(this.value)) {
            toastr.error('No se puede digitar letras en el número de documento.', 'Error', {
                closeButton: true,
                progressBar: true,
                timeOut: 5000,
                positionClass: 'toast-bottom-right'
            });
        }
    });
});