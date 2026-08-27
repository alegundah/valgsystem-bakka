const passwordInput = document.querySelector('#code-input');
const toggleButton = document.querySelector('#togglePassword');


toggleButton.addEventListener('click', function () {

  const isPassword = passwordInput.getAttribute('type') === 'password';
  passwordInput.setAttribute('type', isPassword ? 'text' : 'password');


});