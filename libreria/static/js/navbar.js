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

