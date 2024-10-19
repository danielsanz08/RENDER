function mostrarCambioContraseña() {
    // Mostrar el overlay y la tarjeta
    document.getElementById("cambiar_contraseña").style.display = 'block';
    document.getElementById("overlay").style.display = 'block';
    
    // Desvanecer el overlay
    document.getElementById("overlay").style.opacity = '1'; // Hacer que el overlay sea visible
    
    // Desvanecer el footer y el botón de accesibilidad
    document.querySelector('footer').classList.add('fade-out'); // Asegúrate de que haya un footer
    document.querySelector('#toggle-accessibility-menu').classList.add('fade-out'); // Asegúrate de que el botón de accesibilidad tenga esta clase
}

function cerrarVentana() {
    // Ocultar la tarjeta
    document.getElementById("cambiar_contraseña").style.display = 'none';
    
    // Ocultar el overlay
    document.getElementById("overlay").style.display = 'none';
    document.getElementById("overlay").style.opacity = '0'; // Ocultar el overlay

    // Remover el desvanecimiento del footer y el botón de accesibilidad
    document.querySelector('footer').classList.remove('fade-out');
    document.querySelector('#toggle-accessibility-menu').classList.remove('fade-out');
}
