$(document).ready(function() {
    $('#transaction-form').on('submit', function(event) {
        event.preventDefault(); // Evita el envío inmediato del formulario

        let errorMessages = [];
        const descripcion = $('textarea[name="descripcion"]').val().trim();

        // Validaciones para la descripción
        if (descripcion.length < 5) {
            errorMessages.push('La descripción debe tener al menos 5 caracteres.');
        }
        if (descripcion.length > 20) { // Cambia 20 a la longitud máxima deseada
            errorMessages.push('La descripción no puede contener más de 20 caracteres.');
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

        // Si no hay errores, muestra el popup de éxito
        $('#popup').fadeIn(); // Muestra el popup

        setTimeout(function() {
            $('html, body').animate({
                scrollTop: $('#popup').offset().top - 300 // Ajuste para que el popup quede más arriba
            }, 300); // Desplazamiento suave hacia el popup

            setTimeout(() => {
                $('#popup').fadeOut(); // Oculta el popup después de 2 segundos
                // Enviar el formulario después de que el popup se oculta
                $('#transaction-form')[0].submit(); 
            }, 2000); // Tiempo que el popup se muestra (2 segundos)
        });
    });
});





document.addEventListener('DOMContentLoaded', function() {
    const productosContainer = document.getElementById('productos-container');
    const addProductButton = document.getElementById('agregar-producto');
    const montoTotalInput = document.getElementById('monto-total');

    // Función para actualizar el monto total
    function actualizarMontoTotal() {
        let total = 0;
        const productos = document.querySelectorAll('.producto');

        productos.forEach((producto) => {
            const selectProducto = producto.querySelector('.producto-select');
            const inputCantidad = producto.querySelector('.cantidad-input');
            
            if (selectProducto && inputCantidad) {
                const precio = parseFloat(selectProducto.selectedOptions[0].getAttribute('data-precio')) || 0;
                const cantidad = parseFloat(inputCantidad.value) || 0;
                total += precio * cantidad;
            }
        });

        montoTotalInput.value = total.toFixed(2);
    }

    // Escuchar cambios en todos los selects e inputs de cantidad
    productosContainer.addEventListener('change', function(event) {
        if (event.target.classList.contains('producto-select') || event.target.classList.contains('cantidad-input')) {
            actualizarMontoTotal();
        }
    });

    // Añadir un nuevo producto al hacer clic en el botón
    addProductButton.addEventListener('click', function() {
        const productGroup = document.createElement('div');
        productGroup.classList.add('form-group', 'producto');

        const productoSelect = document.querySelector('.producto-select').cloneNode(true);
        productoSelect.name = 'productos[]';
        productoSelect.required = true;

        const cantidadInput = document.createElement('input');
        cantidadInput.type = 'number';
        cantidadInput.name = 'cantidades[]';
        cantidadInput.placeholder = 'Cantidad';
        cantidadInput.min = '1';
        cantidadInput.required = true;
        cantidadInput.classList.add('cantidad-input');

        productGroup.appendChild(productoSelect);
        productGroup.appendChild(cantidadInput);

        productosContainer.appendChild(productGroup);
    });
});