 // Script para abrir el submenú desde el menú principal
 document.getElementById('openSubMenu').addEventListener('click', function (e) {
    e.preventDefault();
    var mainMenu = bootstrap.Offcanvas.getInstance(document.getElementById('sideMenu'));
    if (mainMenu) mainMenu.hide();

    var subMenu = new bootstrap.Offcanvas(document.getElementById('subMenuTiendas'));
    subMenu.show();
});

// Script para volver al menú principal
document.getElementById('backToMenu').addEventListener('click', function (e) {
    e.preventDefault();
    var subMenu = bootstrap.Offcanvas.getInstance(document.getElementById('subMenuTiendas'));
    if (subMenu) subMenu.hide();

    var mainMenu = new bootstrap.Offcanvas(document.getElementById('sideMenu'));
    mainMenu.show();
});