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
    input.value = input.value.replaceAll(" ", "");
    input.value = input.value.replace(',','.');
    if (!isInt(input.value)){
        $(input).css("background-color", "#ffa1a1");
        $(input).parent().parent().find(".micro_btn.right").attr("disabled", "disabled");
    } else {
        $(input).css("background-color", "#ffffff");
        $(input).parent().parent().find(".micro_btn.right").removeAttr("disabled");
    }
}

function isInt(value) {
    return value >= 0 && !(String(value).replaceAll(" ", "") === "");
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

function details(summary){
    if (summary.innerHTML == "Показать товары"){
        $(summary).html("Скрыть товары");
    }
    else{
        $(summary).html("Показать товары");
    }

}