/* SPARC Lab: shared site behaviour, loaded on every page after jQuery + Bootstrap.
   Handles the nested "Completed Research Area" submenu in the nav bar. */
$(function () {
    // Tapping/clicking the submenu parent also reveals its fly-out (needed on touch screens).
    $('.dropdown-submenu > a').on('click', function (e) {
        $('.dropdown-submenu .dropdown-menu').removeClass('show');
        $(this).next('.dropdown-menu').addClass('show');
        e.stopPropagation();
    });
    // Close any open fly-out when the parent dropdown closes.
    $('.dropdown').on('hidden.bs.dropdown', function () {
        $('.dropdown-menu.show').removeClass('show');
    });
});
