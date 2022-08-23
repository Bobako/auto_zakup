$(document).ready(function () {

});

function addElement(select, el_type) {
    var el_id = select.value;
    if (el_id == "placeholder") {
        return;
    }
    var el = $(select).find('option:selected');
    var el_name = el.text();
    $(el).remove();
    var multi_box = $(select).parent();
    var select_ = $(select);
    $(select).remove()
    select.value = 'placeholder';
    var func = `onclick="removeElement(this, '` + el_type + `')"`;
    multi_box.append("<span class=\"multi_el\" id = \"" + el_id + "\"" + func + ">" + el_name + "</span>");
    multi_box.append(select_)
    var form = $(multi_box.parent().find('.' + el_type));
    form.val(form.val() + el_id + ":");


}

function removeElement(element, el_type) {
    var el_id = element.id;
    console.log(element.textContent);
    var multi_box = $(element).parent();
    var selector = multi_box.find('select');
    selector.append("<option value='" + el_id + "'>" + element.textContent + "</option>");
    var form = multi_box.parent().find('.' + el_type);
    var ids = String(form.val()).split(":");
    ids.splice(ids.indexOf(el_id), 1);
    form.val(ids.join(":"));
    $(element).remove();
}


function fell(btn) {
    let div = $(btn).parent().find(".fell_div");
    let hidden = $(div).hasClass("fell_hidden");
    if (hidden) {
        let position = $(btn).offset();
        $(div).removeClass("fell_hidden");
        $(div).css("top", position.top+btn.high);
        $(div).css("left", position.left - 60);
    } else {
        $(div).addClass("fell_hidden");
    }
}

function live_search(vid, field, e){
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
    req.open("GET", "api/search?s=" + $(field).val(), false);
    req.send(null);

    $(wrapper).empty();
    $(wrapper).append(req.responseText);
}

function addEl(button, pid){
    var multi_box = $(button).parent().parent();
    var func = `onclick="removeElement(this, '` + 'product' + `')"`;
    multi_box.append("<span class=\"multi_el\" id = \"" + pid + "\"" + func + ">" + button.innerHTML + "</span>");
    var form = $(multi_box.parent().find('.' + 'product'));
    form.val(form.val() + pid + ":");
    var field = multi_box.find('input');
    var wrapper = multi_box.find('.advice_wrapper');
    $(field).remove();
    $(wrapper).remove();
    $(multi_box).append(field);
    $(multi_box).append(wrapper);
    multi_box.find('input').val('');
    multi_box.find('.advice_wrapper').empty();
}