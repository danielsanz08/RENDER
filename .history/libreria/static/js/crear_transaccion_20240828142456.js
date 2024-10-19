document.addEventListener('DOMContentLoaded', function() {
    const inputFecha = document.getElementById('fecha');
    const today = new Date().toISOString().split('T')[0];
    inputFecha.setAttribute('min', today);
});

function validateUpdateForm() {
    const nombre = document.getElementById("id_nombre").value.trim(); 
    const cantidad = document.getElementById("id_cantidad").value;
    const originalNombre = document.getElementById("original-nombre").value;
    const fecha = document.getElementById("fecha").value; // El campo de fecha

    toastr.clear();

    let errorMessages = [];
    const nombreRegex = /^[a-zA-Z\s]+$/;

    if (!nombreRegex.test(nombre)) {
        errorMessages.push('El nombre solo puede contener letras y espacios.');
    }

    if (cantidad < 0 || isNaN(cantidad)) {
        errorMessages.push('No se pueden ingresar números negativos.');
    }

    // Validación de la fecha
    const today = new Date();
    const selectedDate = new Date(fecha);
    
    if (selectedDate < today) {
        errorMessages.push('No se puede seleccionar una fecha anterior a hoy.');
    }

    $.ajax({
        url: '/verificar_nombre_insumo/',
        type: 'GET',
        data: { 'nombre': nombre },
        dataType: 'json',
        success: function(response) {
            if (response.exists && nombre !== originalNombre) {
                errorMessages.push('Ya existe un insumo con este nombre.');
            }

            if (errorMessages.length > 0) {
                toastr.error(errorMessages.join('<br>'), 'Error', {
                    closeButton: true,
                    progressBar: true,
                    timeOut: 5000,
                    positionClass: 'toast-bottom-right'
                });
            } else {
                toastr.success('El insumo se ha modificado correctamente.', 'Éxito', {
                    closeButton: true,
                    progressBar: true,
                    timeOut: 5000,
                    positionClass: 'toast-bottom-right'
                });

                setTimeout(function() {
                    document.getElementById("update-insumo-form").submit();
                }, 2000);
            }
        }
    });

    return false;
}
function validateUpdateForm() {
    const nombre = document.getElementById("id_nombre").value.trim(); 
    const cantidad = document.getElementById("id_cantidad").value;
    const originalNombre = document.getElementById("original-nombre").value;
    const fecha = document.getElementById("fecha").value; // El campo de fecha

    toastr.clear();

    let errorMessages = [];
    const nombreRegex = /^[a-zA-Z\s]+$/;

    if (!nombreRegex.test(nombre)) {
        errorMessages.push('El nombre solo puede contener letras y espacios.');
    }

    if (cantidad < 0 || isNaN(cantidad)) {
        errorMessages.push('No se pueden ingresar números negativos.');
    }

    // Validación de la fecha
    const today = new Date();
    const selectedDate = new Date(fecha);
    
    if (selectedDate < today) {
        errorMessages.push('No se puede seleccionar una fecha anterior a hoy.');
    }

    $.ajax({
        url: '/verificar_nombre_insumo/',
        type: 'GET',
        data: { 'nombre': nombre },
        dataType: 'json',
        success: function(response) {
            if (response.exists && nombre !== originalNombre) {
                errorMessages.push('Ya existe un insumo con este nombre.');
            }

            if (errorMessages.length > 0) {
                toastr.error(errorMessages.join('<br>'), 'Error', {
                    closeButton: true,
                    progressBar: true,
                    timeOut: 5000,
                    positionClass: 'toast-bottom-right'
                });
            } else {
                toastr.success('El insumo se ha modificado correctamente.', 'Éxito', {
                    closeButton: true,
                    progressBar: true,
                    timeOut: 5000,
                    positionClass: 'toast-bottom-right'
                });

                setTimeout(function() {
                    document.getElementById("update-insumo-form").submit();
                }, 2000);
            }
        }
    });

    return false;
}
// Función para mostrar la alerta
function mostrarAlerta() {
    document.getElementById("alert").style.display = 'block';
}

// Función para cerrar la ventana de alerta
function cerrarVentana() {
    document.getElementById("alert").style.display = 'none';
}

// Función para manejar el envío del formulario
function enviarFormulario() {
    document.getElementById("transaction-form").submit();
}

// Agregar event listener al formulario para prevenir el envío por defecto
document.getElementById("transaction-form").addEventListener("submit", function(event) {
    event.preventDefault();
    mostrarAlerta();
});

// Modificar la alerta para incluir botones de confirmación y cancelación
document.getElementById("alert").innerHTML = `
    <i class="fas fa-exclamation-triangle" id="alerta-icono"></i>
    <p><h4>¿Estás seguro de que quieres registrar esta transacción?</h4></p>
    <button onclick="enviarFormulario()"><h3>Confirmar</h3></button>
    <button onclick="cerrarVentana()"><h3>Cancelar</h3></button>
`;