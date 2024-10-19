document.addEventListener('DOMContentLoaded', () => {
    const accessibilityMenu = document.getElementById('accessibility-menu');
    const toggleAccessibilityMenuBtn = document.getElementById('toggle-accessibility-menu');
    const zoomInBtn = document.getElementById('zoom-in');
    const zoomOutBtn = document.getElementById('zoom-out');
    const zoomResetBtn = document.getElementById('zoom-reset');
    const zoomPercentageDisplay = document.getElementById('zoom-percentage');
    const darkModeButton = document.getElementById('dark-mode-button');
    const monochromeButton = document.getElementById('monochrome-mode-button');

    // Mostrar u ocultar el menú de accesibilidad basado en el estado almacenado
    const isMenuVisible = localStorage.getItem('accessibilityMenuVisible') === 'true';
    accessibilityMenu.style.display = isMenuVisible ? 'block' : 'none';

    // Alternar visibilidad del menú de accesibilidad
    toggleAccessibilityMenuBtn.addEventListener('click', () => {
        const isCurrentlyVisible = accessibilityMenu.style.display === 'block';
        accessibilityMenu.style.display = isCurrentlyVisible ? 'none' : 'block';
        localStorage.setItem('accessibilityMenuVisible', !isCurrentlyVisible);
    });

    // Configurar el nivel de zoom inicial
    let currentZoom = parseInt(localStorage.getItem('zoomLevel')) || 100;

    // Seleccionar todos los elementos de texto que deseas ajustar
    const textElements = document.querySelectorAll('body *:not(#accessibility-menu):not(#accessibility-menu *)');

    // Aplicar el nivel de zoom inicial a todos los elementos seleccionados
    applyZoom(currentZoom);

    zoomPercentageDisplay.textContent = `${currentZoom}%`;

    // Función para aplicar el zoom a los elementos de texto
    function applyZoom(zoomLevel) {
        textElements.forEach(el => {
            const originalSize = el.getAttribute('data-original-size') || window.getComputedStyle(el).fontSize; // Obtener el tamaño original
            if (!el.getAttribute('data-original-size')) {
                el.setAttribute('data-original-size', originalSize); // Guardar el tamaño original como atributo de datos
            }
            el.style.fontSize = `${(zoomLevel / 100) * parseFloat(el.getAttribute('data-original-size'))}px`; // Ajustar el tamaño
        });
    }

    // Función para cambiar el zoom
    function changeZoom(amount) {
        let newZoom = currentZoom + amount;
        if (newZoom >= 50 && newZoom <= 150) {
            currentZoom = newZoom;
            applyZoom(currentZoom);
            localStorage.setItem('zoomLevel', currentZoom);
            zoomPercentageDisplay.textContent = `${currentZoom}%`;
        }
    }

    // Función para resetear el zoom
    function resetZoom() {
        currentZoom = 100;
        textElements.forEach(el => {
            if (el.getAttribute('data-original-size')) {
                el.style.fontSize = el.getAttribute('data-original-size'); // Restablecer al tamaño original
            }
        });
        localStorage.setItem('zoomLevel', currentZoom);
        zoomPercentageDisplay.textContent = '100%';
    }

    // Event Listeners para los botones de zoom
    zoomInBtn.addEventListener('click', () => changeZoom(10));
    zoomOutBtn.addEventListener('click', () => changeZoom(-10));
    zoomResetBtn.addEventListener('click', resetZoom);



    // Aplicar el tema oscuro basado en el estado almacenado
    const isDarkModeEnabled = localStorage.getItem('dark-mode') === 'true';
    if (isDarkModeEnabled) {
        document.body.classList.add('dark-mode');
    }

    // Alternar el tema oscuro y guardarlo en el almacenamiento local
    darkModeButton.addEventListener('click', () => {
        const isDarkModeEnabled = document.body.classList.toggle('dark-mode');
        localStorage.setItem('dark-mode', isDarkModeEnabled);
    });

    // Aplicar el modo monocromo basado en el estado almacenado
    const isMonochromeModeEnabled = localStorage.getItem('monochrome-mode') === 'true';
    if (isMonochromeModeEnabled) {
        document.body.classList.add('monochrome-mode');
    }

    // Alternar el modo monocromo y guardarlo en el almacenamiento local
    monochromeButton.addEventListener('click', () => {
        const isMonochromeModeEnabled = document.body.classList.toggle('monochrome-mode');
        localStorage.setItem('monochrome-mode', isMonochromeModeEnabled);
    });



    // Función para resaltar títulos
    window.toggleHighlightTitles = function() {
        document.body.classList.toggle('highlight-titles');
        // Guardar la preferencia en localStorage
        const isHighlightActive = document.body.classList.contains('highlight-titles');
        localStorage.setItem('highlightTitles', isHighlightActive);
    };

    // Al cargar la página, aplicar la preferencia de resaltar títulos
    const highlightTitles = localStorage.getItem('highlightTitles') === 'true';
    if (highlightTitles) {
        document.body.classList.add('highlight-titles');
    }

    // Opción de resaltar enlaces
    const highlightLinksButton = document.getElementById('highlight-links-button');
    highlightLinksButton.addEventListener('click', function () {
        document.querySelectorAll('a').forEach(link => {
            link.classList.toggle('highlighted-link'); // Añade o quita la clase de resaltado
        });
        
        // Guardar el estado de resaltado en localStorage
        const isHighlighted = highlightLinksButton.classList.contains('highlighted-link');
        localStorage.setItem('highlightLinks', isHighlighted ? 'enabled' : 'disabled');
    });

    // Cargar el estado de resaltado al cargar la página
    if (localStorage.getItem('highlightLinks') === 'enabled') {
        document.querySelectorAll('a').forEach(link => {
            link.classList.add('highlighted-link');
        });
    }

    // Fuente legible
    const readableFontButton = document.getElementById('readable-font-button');
    let isReadableFontEnabled = localStorage.getItem('readableFont') === 'true';

    // Aplicar el estado de la fuente legible al cargar
    if (isReadableFontEnabled) {
        document.body.classList.add('readable-font');
    }

    readableFontButton.addEventListener('click', function() {
        isReadableFontEnabled = !isReadableFontEnabled;
        document.body.classList.toggle('readable-font', isReadableFontEnabled);
        
        // Guardar el estado en localStorage
        localStorage.setItem('readableFont', isReadableFontEnabled);
    });
});
