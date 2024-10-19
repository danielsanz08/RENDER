$(document).ready(function() {
    $('#register-form').on('submit', function(event) {
        event.preventDefault(); // Evita el envío inmediato del formulario

        let errorMessages = [];
        const nombre = $('#name').val().trim();
        const email = $('#email').val().trim();
        const role = $('#role').val();
        const phone = $('#phone').val().trim();
        const password = $('#password').val();
        const confirmPassword = $('#confirm_password').val();

        // Expresiones regulares
        const nombreRegex = /^[A-Za-zÁáÉéÍíÓóÚúÑñ\s]+$/; // Solo letras y espacios
        const emailRegex = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/; // Validación de correo
        const phoneRegex = /^[0-9]{10}$/; // Validación de teléfono (10 dígitos)

        // Validaciones
        if (!nombreRegex.test(nombre)) {
            errorMessages.push('El nombre solo puede contener letras y espacios.');
        }

        if (!emailRegex.test(email)) {
            errorMessages.push('Por favor, ingresa un correo electrónico válido.');
        }

        if (role === "") {
            errorMessages.push('Debes seleccionar un rol.');
        }

        if (!phoneRegex.test(phone)) {
            errorMessages.push('El teléfono debe contener 10 dígitos numéricos.');
        }

        // Validación de contraseña segura
        const passwordValidation = validatePassword(password);
        if (!passwordValidation.isValid) {
            errorMessages.push(passwordValidation.message);
        }

        if (password !== confirmPassword) {
            errorMessages.push('Las contraseñas no coinciden.');
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
                $('#register-form')[0].submit(); 
            }, 2000); // Tiempo que el popup se muestra (2 segundos)
        });
    });

    // Función para validar la contraseña
    function validatePassword(password) {
        const minLength = 8;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /[0-9]/.test(password);
        const hasSpecialChars = /[!@#$%^&*(),.?":{}|<>]/.test(password);
        const isValid = password.length >= minLength && hasUpperCase && hasLowerCase && hasNumbers && hasSpecialChars;
        
        let message = '';
        if (password.length < minLength) {
            message += `La contraseña debe tener al menos ${minLength} caracteres.<br>`;
        }
        if (!hasUpperCase) {
            message += 'La contraseña debe contener al menos una letra mayúscula.<br>';
        }
        if (!hasLowerCase) {
            message += 'La contraseña debe contener al menos una letra minúscula.<br>';
        }
        if (!hasNumbers) {
            message += 'La contraseña debe contener al menos un número.<br>';
        }
        if (!hasSpecialChars) {
            message += 'La contraseña debe contener al menos un carácter especial.<br>';
        }

        return { isValid, message };
    }

    // Mostrar mensaje de validación de contraseña en tiempo real
    $('#password').on('input', function() {
        const password = $(this).val();
        const passwordValidation = validatePassword(password);

        // Actualizar el mensaje de validación debajo del input
        const feedback = $('#passwordFeedback'); // Cambié esto a jQuery para asegurarme de que funciona correctamente

        if (!passwordValidation.isValid) {
            feedback.html(passwordValidation.message).css('color', 'red').show();
        } else {
            feedback.html('Contraseña segura').css('color', 'green').show();
        }
    });

    // Función para comparar las contraseñas y mostrar un mensaje si no coinciden
    $('#confirm_password').on('input', function() {
        const password = $('#password').val();
        const confirmPassword = $(this).val();
        const feedbackConfirm = $('#confirmPasswordFeedback');

        if (password !== confirmPassword && confirmPassword.length > 0) {
            feedbackConfirm.html("<span style='color: red;'>Las contraseñas no coinciden</span>");
        } else if (password === confirmPassword && confirmPassword.length > 0) {
            feedbackConfirm.html("<span style='color: green;'>Las contraseñas coinciden</span>");
        } else {
            feedbackConfirm.html("");
        }
    });
});
