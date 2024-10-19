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
// Muestra la ventana emergente
function mostrarPopup() {
    const popup = document.getElementById('popup');
    popup.style.display = 'flex';
    setTimeout(() => {
        popup.style.display = 'none';
    }, 3000); // Oculta la ventana emergente después de 3 segundos
}