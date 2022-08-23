$(document).ready(function () {
    var oid = $("#order_id").val();
    var msgs = $('textarea');
    for (let i = 0; i < msgs.length; i++){
        set_msg(oid, msgs[i]);
    }


});

function set_msg(oid, msg){
    var vid = msg.id;
    var req = new XMLHttpRequest();
    req.open("GET", "/api/formatted_order?oid=" + String(oid) + "&vid=" + String(vid), false);
    req.send(null);
    msg.append(req.responseText);
}