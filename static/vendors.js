$(document).ready(function () {

});

function addElement(select, el_type) {
    var el_id = select.value;
    if (el_id == "placeholder") {
        return;
    }
    var el_name = $(select).find('option:selected')
    el_name = el_name.text();
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
    var multi_box = $(element).parent();
    var form = multi_box.parent().find('.' + el_type);
    var ids = String(form.val()).split(":");
    console.log(ids);
    ids.splice(ids.indexOf(el_id), 1);
    console.log(ids);
    form.val(ids.join(":"));
    $(element).remove();
}