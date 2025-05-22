// Toggle password visibility for the password1 field
document.getElementById('togglePassword').addEventListener('click', function () {
  const pwd1 = document.getElementById('id_password1');
  const icon1 = document.getElementById('togglePasswordIcon');

  const show = pwd1.type === 'password';
  pwd1.type = show ? 'text' : 'password';
  icon1.classList.toggle('bi-eye-slash');
  icon1.classList.toggle('bi-eye');
});

// Toggle password visibility for the password2 field
document.getElementById('togglePasswordConfirmation').addEventListener('click', function () {
  const pwd2 = document.getElementById('id_password2');
  const icon2 = document.getElementById('togglePasswordConfirmationIcon');

  const show = pwd2.type === 'password';
  pwd2.type = show ? 'text' : 'password';
  icon2.classList.toggle('bi-eye-slash');
  icon2.classList.toggle('bi-eye');
});
