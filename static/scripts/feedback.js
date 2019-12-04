// var data = [
//     {
//         'name': '张三',
//         'tel': '13512345678',
//         'street': '碧岭街道',
//         'community': '碧岭社区',
//         'property': '建议',
//         'content': '随便写点东西。'
//     },
//     {
//         'name': '赵四',
//         'tel': '13554245678',
//         'street': '碧岭街道',
//         'community': '碧岭社区',
//         'content': '拒绝996！！！'
//     }
// ]
// var status = 'success'

// 数据格式参照上面的 data，确认没问题就可以删掉这堆东西了

toastr.options = {
    "closeButton": true,
    "debug": true,
    "positionClass": "toast-top-right",
    "showDuration": "300",
    "hideDuration": "1000",
    "timeOut": "5000",
    "extendedTimeOut": "1000",
    "showEasing": "swing",
    "hideEasing": "linear",
    "showMethod": "fadeIn",
    "hideMethod": "fadeOut"
}

$(document).ready(function () {
    // $.get("", function (data, status) {     // 填读取未录入反馈的路由
    //     if (status === "success" && data) {
    if (data.length === 0) {
        $(".card-body").after("<div class='card-body p-0 pb-3 text-center' align='center'><p>恭喜，您已经录入完所有信息！</p></div>");
    } else {
        for (var i in data) {
            var time = data[i]['time'];
            var name = data[i]['name'];
            var tel = data[i]['tel'];
            var street = data[i]['street'];
            var community = data[i]['community'];
            var property = data[i]['property'];
            var content = data[i]['content'];
            $("tbody").append("<tr>" +
                "<td>" + time + "</td>" +
                "<td>" + name + "</td>" +
                "<td>" + tel + "</td>" +
                "<td>" + street + "</td>" +
                "<td>" + community + "</td>" +
                "<td>" + property + "</td>" +
                "<td width='18%'><div class='text-justify'>" + content + "</div></td>" +
                "<td width='10%'><input class='form-control'></td>" +
                "<td width='10%'><input class='form-control'></td>" +
                "<td width='10%'><input class='form-control'></td>" +
                "<td width='10%'><input class='form-control'></td>" +
                "<td><div class='btn-group'><button class='btn btn-sm btn-primary' id='submit'>提交</button><button class='btn btn-sm btn-danger' id='delete'>删除</button></div></td>" +
                "</tr>")
        }
    }
    // }
    // })
    $("#submit").click(function () {
        var tr = $(this).closest("tr");
        var td = tr.children("td");
        var event_type = td.eq(7).children("input").val();
        var main_type = td.eq(8).children("input").val();
        var sub_type = td.eq(9).children("input").val();
        var dispose_unit = td.eq(10).children("input").val();
        if (event_type === '' || main_type === '' || sub_type === '' || dispose_unit === '') {
            toastr.info("请将表格填写完整！");
        } else {
            var data = {
                'time': td.eq(0).text(),
                'name': td.eq(1).text(),
                'tel': td.eq(2).text(),
                'street': td.eq(3).text(),
                'community': td.eq(4).text(),
                'property': td.eq(5).text(),
                'event-type': event_type,
                'main-type': main_type,
                'sub-type': sub_type,
                'dispose-unit': dispose_unit
            };
            $.post("../store_feedback/", data);   // 填录入反馈的路由
            // console.log(data);
            tr.remove();
            toastr.success("提交成功");
            if ($("tbody").children("tr").length === 0) {
                $(".card-body").after("<div class='card-body p-0 pb-3 text-center' align='center'><p>恭喜，您已经录入完所有信息！</p></div>");
            }
        }
    })
    $("#delete").click(function () {
        var tr = $(this).closest("tr");
        var td = tr.children("td");
        var data = {
            'time': td.eq(0).text(),
            'name': td.eq(1).text(),
            'tel': td.eq(2).text(),
            'street': td.eq(3).text(),
            'community': td.eq(4).text(),
            'property': td.eq(5).text(),
            'event-type': td.eq(7).children("input").val(),
            'main-type': td.eq(8).children("input").val(),
            'sub-type': td.eq(9).children("input").val(),
            'dispose-unit': td.eq(10).children("input").val()
        };
        $.post("../delete_feedback/", data);   // 填录入反馈的路由
        // console.log(data);
        tr.remove();
        toastr.success("删除成功");
        if ($("tbody").children("tr").length === 0) {
            $(".card-body").after("<div class='card-body p-0 pb-3 text-center' align='center'><p>恭喜，您已经录入完所有信息！</p></div>");
        }
    })
})