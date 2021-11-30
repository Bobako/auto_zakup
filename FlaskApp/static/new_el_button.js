$(document).ready(function () {

    var hidden;

    if ($('body').width() < 1510) {
        hidden = true;
        $('nav div').css('left', $('nav div').width() + 30);
        $('.nav_button').css('left', $('nav div').width() - 16);
    } else {
        hidden = false;
    }

    $(".nav_button").click(function () {
        if (hidden) {
            $('nav div').css('left', '');
            $('.nav_button').css('left', '');
            hidden = false;
        } else {
            hidden = true;
            $('nav div').css('left', $('nav div').width() + 30);
            $('.nav_button').css('left', $('nav div').width() - 16);
        }

    });


    $("#new_el_button").click(function () {
        $(".template").clone().toggleClass("template db_el").appendTo("#new_el_div");

    });
});