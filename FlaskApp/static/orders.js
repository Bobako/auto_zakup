$(document).ready(function () {
    var selector = $("#new_order_facility");
    get_available_products(selector);

    $(window).keydown(function(event){
    if(event.keyCode == 13) {
      event.preventDefault();
      return false;
    }
  });

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

function addProduct(button, pid){
    let els = $(".pid"+pid);
    if (!$(els).is("[hidden]")){
        return
    }
    console.log(".pid"+pid);
    els.remove();
    var form = $(button).parent().parent().find('.products');
    form.append(els);
    form.append("<br>")
    $(".pid"+pid).removeAttr("hidden");
    $(button).parent().parent().find(".live_search").val('');
    $(button).parent().empty();

}

function details(summary){
    if (summary.innerHTML == "Показать товары"){
        $(summary).html("Скрыть товары");
    }
    else{
        $(summary).html("Показать товары");
    }

}

function live_search(oid, field, e){
    if (e.key == "Enter"){
        return;
    }

    if ($(field).val().length < 2){
        let wrapper = $(field).parent().find('.advice_wrapper');
        $(wrapper).empty();
        return;
    }
    let wrapper = $(field).parent().find('.advice_wrapper');
    var req = new XMLHttpRequest();
    req.open("GET", "/api/order_search?oid="+String(oid) +"&s=" + $(field).val(), false);
    req.send(null);

    $(wrapper).empty();
    $(wrapper).append(req.responseText);
}