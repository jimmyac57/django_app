 // Toggle password visibility for the password field
 document.getElementById('togglePassword').addEventListener('click', function () {
    const passwordField = document.getElementById('password');
    const toggleIcon = document.getElementById('togglePasswordIcon');

    // Toggle the type attribute
    const isPassword = passwordField.getAttribute('type') === 'password';
    passwordField.setAttribute('type', isPassword ? 'text' : 'password');

    // Toggle the icon
    toggleIcon.classList.toggle('bi-eye-slash');
    toggleIcon.classList.toggle('bi-eye');
});

// Toggle password visibility for the password confirmation field
document.getElementById('togglePasswordConfirmation').addEventListener('click', function () {
    const passwordConfirmationField = document.getElementById('password_confirmation');
    const toggleIcon = document.getElementById('togglePasswordConfirmationIcon');

    // Toggle the type attribute
    const isPassword = passwordConfirmationField.getAttribute('type') === 'password';
    passwordConfirmationField.setAttribute('type', isPassword ? 'text' : 'password');

    // Toggle the icon
    toggleIcon.classList.toggle('bi-eye-slash');
    toggleIcon.classList.toggle('bi-eye');
});