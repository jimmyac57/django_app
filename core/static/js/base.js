document.querySelectorAll('.nav-right > li > a').forEach((item) => {
    item.addEventListener('click', (e) => {
        const subMenu = item.nextElementSibling; // Buscar el submenú asociado
        if (subMenu) {
            e.preventDefault(); // Evitar redirección del enlace

            // Cerrar todos los submenús abiertos
            document.querySelectorAll('.nav-right li ul.visible').forEach((menu) => {
                if (menu !== subMenu) {
                    menu.classList.remove('visible'); // Ocultar otros submenús
                    const icon = menu.previousElementSibling.querySelector('.toggle-icon');
                    if (icon) {
                        icon.classList.remove('rotated'); // Resetear el ícono
                    }
                }
            });

            // Alternar visibilidad del submenú actual
            subMenu.classList.toggle('visible');

            // Alternar rotación del ícono
            const icon = item.querySelector('.toggle-icon');
            if (icon) {
                icon.classList.toggle('rotated');
            }
        }
    });
});
