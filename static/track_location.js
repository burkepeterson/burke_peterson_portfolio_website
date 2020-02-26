$(window).on('activate.bs.scrollspy', function(e) {
    history.pushState({}, "", $('.nav-item .active').attr("href"))
});