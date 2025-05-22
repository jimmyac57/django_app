// Toggle password visibility for the password1 field
document.getElementById('togglePassword').addEventListener('click', function () {
  const pwd1 = document.getElementById('id_password');
  const icon1 = document.getElementById('togglePasswordIcon');

  const show = pwd1.type === 'password';
  pwd1.type = show ? 'text' : 'password';
  icon1.classList.toggle('bi-eye-slash');
  icon1.classList.toggle('bi-eye');
});
