$(document).ready(function(){
    $('.list_lh li:even').addClass('lieven');
})

$(function(){
    $("div.list_lh").myScroll({
        speed:40, //数值越大，速度越慢
        rowHeight:68 //li的高度
    });
});

toastr.options = {
    "closeButton": true,
    "debug": true,
    "positionClass": "toast-top-right",
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "3600000",
    "extendedTimeOut": "60000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}

self.setInterval("getEvent()", 1000);

function getEvent() {
    $.get("/scroll_display", function (data, status) {
        if (status === "success" && data) {
            console.log(data);
            console.log(typeof data)
            var obj = JSON.parse(data)
            var time = obj['time'];
            var street = obj['street'];
            var community = obj['community'];
            var src = obj['src'];
            var event = obj['event'];
            var property = obj['property'];
            var dispose_unit = obj['dispose_unit'];
            // $(".list_lh").children("ul").append("<li><p>" + data + "</p></li>");
            $(".list_lh").children("ul").append("<li style=\"font-size: medium\">" + time + " " + 
                                                    "<span class=\"street\">" + street + "</span> 的 " +
                                                    "<span class=\"community\">" + community + "</span> 从 " + 
                                                    "<span class=\"channel\">" + src + "</span> 接到 " + 
                                                    "<span class=\"things\">" + event + "</span> " +
                                                    "<span class=\"type\">" + property + "</span>，请 " +
                                                    "<span class=\"duty\">" + dispose_unit + "</span> 尽快前往处理。" +
                                                "</li>")
            $('.list_lh li:even').addClass('lieven');
            $('.list_lh li:odd').removeClass('lieven');
        }
    })
}

self.setInterval("getAlert()", 5000);

function getAlert() {
    $.get("/abnormal_events", function (data, status) {
        if (status === "success" && data) {
            toastr.error(data);
        }
    })
}