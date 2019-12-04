$("#chart").ready(function () {
    var chart = echarts.init($("#chart")[0]);
    var option = {
        tooltip: {
            trigger: 'axis',
            axisPointer: {            // 坐标轴指示器，坐标轴触发有效
                type: 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
            }
        },
        legend: {
            data: typename
        },
        grid: {
            left: '3%',
            right: '4%',
            bottom: '3%',
            containLabel: true
        },
        xAxis: {
            type: 'value'
        },
        yAxis: {
            type: 'category',
            data: street
        },
        series: []
    };
    for (var i = 0; i < typename.length; i++) {
        option["series"].push({
            name: typename[i],
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: false,
                    position: 'insideRight'
                }
            },
            data: data[i]
        })
    }
    chart.setOption(option);
});

$(window).resize(function () {
    echarts.init($("#chart")[0]).resize();
});
