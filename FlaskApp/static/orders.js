$(document).ready(function () {
    var selector = $("#new_order_facility");
    get_available_products(selector);


});

function squ(input){
    alert("jej");
}




function get_available_products(selector) {
    var fac_id = $(selector).val();
    if (fac_id == "placeholder") {
        return;
    }




    var req = new XMLHttpRequest();
    req.open("GET", "/api/available_products?id=" + String(fac_id), false);
    req.send(null);
    $("#new_order_placeholder").empty();
    $("#new_order_placeholder").append(req.responseText);
}


function checkAmount(input) {
    if (!isInt(input.value)){
        $(input).css("background-color", "#ffa1a1");
        $(input).parent().parent().find(".micro_btn.right").attr("disabled", "disabled");
    } else {
        $(input).css("background-color", "#ffffff");
        $(input).parent().parent().find(".micro_btn.right").removeAttr("disabled");
    }
}

function isInt(value) {
    return !isNaN(value) &&(function (x) {
        return ((x | 0) === x) && x>=0;
    })(parseFloat(value))
}

function selectFacility(selector){
    var fac_id = $(selector).val();

    window.location.href = "/?fid="+String(fac_id);
}

function addProduct(selector){
    var pid = $(selector).val();
    if (pid == "placeholder"){
        return;
    }

    var el = $(selector).find('option:selected');
    $(el).remove();

    let els = $("."+pid);
    els.remove();
    var form = $(selector).parent().find('.products');
    form.append(els);
    form.append("<br>")
    $("."+pid).removeAttr("hidden");


}