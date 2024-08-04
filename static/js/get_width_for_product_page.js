var width = $(".product-page-image").width();
var width_container = $(".container").width();

if (document.width > 768) {
    $(".product-page-data").css({
        "width": (width_container - width) + "px"
    });
};