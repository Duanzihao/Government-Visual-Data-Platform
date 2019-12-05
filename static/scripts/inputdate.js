// var mode = 1;
if (mode == 1) {
    var start = '1970-01-01';
} else {
    var start = '2018-10-01';
}
// var datemode = "3"
// var startDate = '2018-2';
// var endDate = '';

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

$(".input-month").ready(function () {
    $(".input-month").each(function () {
        $(this).datepicker({
            language: 'zh-CN',
            autoclose: true,
            clearBtn: true,
            format: 'yyyy-mm',
            startView: 1,
            minViewMode: 1,
            startDate: '1970-01',
            endDate: '2018-10'
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

$("#dateform").submit(function () {
    var startDate = new Date($("#startDate").val());
    var endDate = new Date($("#endDate").val());
    if (endDate < startDate) {
        toastr.warning("请输入正确的时间范围");
        event.preventDefault();
        event.stopPropagation();
    }
})

if (datemode === "1") {
    $("#collapseOne").addClass('show');
    $("#startDate").val(startDate);
    $("#endDate").val(endDate);
    $("#collapseTwo").removeClass('show');
    $("#collapseThree").removeClass('show');
} else if (datemode === "2") {
    $("#collapseTwo").addClass('show');
    $("#startMonth").val(startDate);
    $("#collapseOne").removeClass('show');
    $("#collapseThree").removeClass('show');
} else if (datemode === "3") {
    $("#collapseThree").addClass('show');
    var date = startDate.split("-");
    $("#year-season").val(date[0]);
    $("#season").val(date[1]);
    $("#collapseOne").removeClass('show');
    $("#collapseTwo").removeClass('show');
}