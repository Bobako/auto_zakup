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