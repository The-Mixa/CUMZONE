$(document).on('click', 'a.page-scroll', function (event) {
    var $anchor = $(this);
    $('html, body').stop().animate({
        scrollTop: $($anchor.attr('href')).offset().top - 50
    }, 800, 'easeInOutExpo');
    event.preventDefault();
});


$('.navbar-nav a').on('click', function () {
    if ($('.navbar-toggle').css('display') != 'none') {
        $(".navbar-toggle").trigger("click");
    }
});