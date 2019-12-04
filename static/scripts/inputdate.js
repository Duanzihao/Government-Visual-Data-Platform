if (mode == 1) {
    var start = '1970-01-01';
} else {
    var start = '2018-10-01';
}

$(".input-date").ready(function () {
    $(".input-date").each(function () {
        $(this).datepicker({
            language: 'zh-CN',
            autoclose: true,
            clearBtn: true,
            format: 'yyyy-mm-dd',
            startDate: start,
            endDate: '2018-10-30'
        });
    });
});

toastr.options = {
    "closeButton": true,
    "debug": true,
    "positionClass": "toast-top-center",
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}

$("form").submit(function () {
    var startDate = new Date($("#startDate").val());
    var endDate = new Date($("#endDate").val());
    if (endDate.getDate() < startDate.getDate()) {
        toastr.warning("请输入正确的时间范围");
        event.preventDefault();
        event.stopPropagation();
    }
})