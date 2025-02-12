document.getElementById('loginForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Evita que se envíe el formulario inmediatamente
    const button = document.querySelector('.transition-button');
    button.classList.add('loading'); // Añade la clase de carga

    // Simula un tiempo de carga de 3 segundos
    setTimeout(() => {
        button.classList.remove('loading'); // Elimina la clase de carga
        this.submit(); // Envía el formulario después de la animación
    }, 500);
});



const togglePassword = document.getElementById('togglePassword');
const passwordField = document.getElementById('password');

togglePassword.addEventListener('click', function () {
  // Alternar el tipo de input entre "password" y "text"
  const type = passwordField.type === 'password' ? 'text' : 'password';
  passwordField.type = type;
  // Cambiar el ícono
  this.classList.toggle('fa-eye-slash');
});
