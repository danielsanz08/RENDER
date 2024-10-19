// Función para evaluar la fortaleza de la contraseña y mostrar mensajes cortos según lo que falta
function evaluarContrasena() {
    const newPassword = document.getElementById('newPassword').value;
    const feedback = document.getElementById('passwordFeedback');

    // Requisitos de la contraseña
    const requisitos = {
        longitud: newPassword.length >= 8,
        mayuscula: /[A-Z]/.test(newPassword),
        minuscula: /[a-z]/.test(newPassword),
        numero: /\d/.test(newPassword),
        especial: /[@$!%*?&]/.test(newPassword)
    };

    // Mensaje de feedback según lo que falta
    let mensajes = [];
    if (!requisitos.longitud) mensajes.push("Al menos 8 caracteres");
    if (!requisitos.mayuscula) mensajes.push("una mayúscula");
    if (!requisitos.minuscula) mensajes.push("una minúscula");
    if (!requisitos.numero) mensajes.push("un número");
    if (!requisitos.especial) mensajes.push("y un carácter especial");

    if (mensajes.length === 0) {
        feedback.innerHTML = "<span style='color: green;'>Contraseña segura</span>";
    } else {
        feedback.innerHTML = "<span style='color: red;'>Utiliza: " + mensajes.join(", ") + "</span>";
    }
}

// Función para ocultar el mensaje de "Contraseña segura" al cambiar de campo
function ocultarMensajeSeguro() {
    const feedback = document.getElementById('passwordFeedback');
    // Solo ocultar el mensaje si es el de "Contraseña segura"
    if (feedback.innerHTML.includes("Contraseña segura")) {
        feedback.innerHTML = "";
    }
}

// Función para comparar las contraseñas y mostrar un mensaje si no coinciden
function compararContrasenas() {
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const feedbackConfirm = document.getElementById('confirmPasswordFeedback');

    if (newPassword !== confirmPassword && confirmPassword.length > 0) {
        feedbackConfirm.innerHTML = "<span style='color: red;'>Las contraseñas no coinciden</span>";
    } else if (newPassword === confirmPassword && confirmPassword.length > 0) {
        feedbackConfirm.innerHTML = "<span style='color: green;'></span>";
    } else {
        feedbackConfirm.innerHTML = "";
    }
}

// Función para validar la contraseña antes de enviar el formulario
function validarContrasena() {
    const newPassword = document.getElementById('newPassword').value;
    const confirmPassword = document.getElementById('confirmPassword').value;
    const mensaje = document.getElementById('messageAlert');

    const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;

    if (!regex.test(newPassword)) {
        mensaje.textContent = "Contraseña no válida.";
        mensaje.classList.remove('hide');
        return false;
    } else {
        mensaje.classList.add('hide');
    }

    if (newPassword !== confirmPassword) {
        mensaje.textContent = "No coinciden.";
        mensaje.classList.remove('hide');
        return false;
    }

    return true; // Si todo es correcto, se envía el formulario
}

// Asociar eventos a los inputs
document.getElementById('newPassword').addEventListener('input', evaluarContrasena);
document.getElementById('newPassword').addEventListener('blur', ocultarMensajeSeguro);
document.getElementById('confirmPassword').addEventListener('input', compararContrasenas);
