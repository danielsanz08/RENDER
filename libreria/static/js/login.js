let container = document.getElementById('container')

toggle = () => {
	container.classList.toggle('sign-in')
	container.classList.toggle('sign-up')
}

setTimeout(() => {
	container.classList.add('sign-in')
}, 200)

function togglePassword() {
	const passwordInput = document.getElementById('id_password');
	const toggleButton = document.getElementById('togglePassword');
	
	if (passwordInput.type === 'password') {
		passwordInput.type = 'text';
		toggleButton.innerHTML = '<i class="bi bi-eye-fill"></i>'; // Cambiar icono a ojo abierto
	} else {
		passwordInput.type = 'password';
		toggleButton.innerHTML = '<i class="bi bi-eye-slash-fill"></i>'; // Cambiar icono a ojo cerrado
	}
}

function togglePasswordVisibility() {
	const passwordInput = document.getElementById('id_password');
	const toggleButton = document.getElementById('togglePassword');

	// Mostrar el botón solo si hay texto en el campo de contraseña
	if (passwordInput.value.length > 0) {
		toggleButton.style.display = 'inline-block';
	} else {
		toggleButton.style.display = 'none';
	}
}