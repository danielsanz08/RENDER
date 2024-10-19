// Cuando el documento HTML se carga completamente, ejecuta este código
document.addEventListener("DOMContentLoaded", function () {
  // Obtiene el icono de accesibilidad y el menú de accesibilidad del DOM
  const accIcon = document.getElementById("acc-icon");
  const accesibilidadMenu = document.getElementById("accesibilidad");

  // Función para mostrar u ocultar el menú de accesibilidad
  function toggleMenu() {
    // Si el menú está oculto o no tiene estilo de visualización, lo muestra
    if (accesibilidadMenu.style.display === "none" || accesibilidadMenu.style.display === "") {
      accesibilidadMenu.style.display = "block"; // Muestra el menú
    } else {
      accesibilidadMenu.style.display = "none"; // Oculta el menú
    }
  }

  // Cuando se hace clic en el icono de accesibilidad, alterna la visibilidad del menú
  accIcon.addEventListener("click", function (event) {
    event.stopPropagation(); // Evita que el clic se propague a otros elementos
    toggleMenu(); // Muestra u oculta el menú
  });

  // Cierra el menú de accesibilidad si se hace clic fuera de él
  document.addEventListener('click', function (event) {
    // Verifica si el clic fue dentro del menú o en el icono
    const isClickInsideMenu = accesibilidadMenu.contains(event.target);
    const isClickOnIcon = accIcon.contains(event.target);

    // Si el clic no fue dentro del menú ni en el icono, oculta el menú
    if (!isClickInsideMenu && !isClickOnIcon && accesibilidadMenu.style.display === "block") {
      accesibilidadMenu.style.display = "none";
    }
  });

  // Evita que al hacer clic dentro del menú, éste se cierre
  accesibilidadMenu.addEventListener('click', function (event) {
    event.stopPropagation();
  });
});

// Muestra u oculta el menú de usuario cuando se hace clic en la imagen del usuario
document.querySelector('.user img').addEventListener('click', function () {
  const menu = document.querySelector('.user-menu');
  // Alterna entre mostrar y ocultar el menú de usuario
  menu.style.display = menu.style.display === 'block' ? 'none' : 'block';
});

// Si se hace clic en cualquier parte fuera del menú de usuario, lo oculta
document.addEventListener('click', function (event) {
  const userMenu = document.getElementById('user-menu');
  const userAvatar = document.getElementById('user-avatar');

  // Si el clic no fue en el menú de usuario ni en el avatar, oculta el menú
  if (!userMenu.contains(event.target) && !userAvatar.contains(event.target)) {
    userMenu.style.display = 'none';
  }
});

// Muestra el menú de usuario cuando se hace clic en el avatar
document.getElementById('user-avatar').addEventListener('click', function () {
  const userMenu = document.getElementById('user-menu');
  userMenu.style.display = 'block'; // Muestra el menú de usuario
});

