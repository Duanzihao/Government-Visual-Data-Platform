$("#chart").ready(function () {
    var data_dict = [];
    for (var i = 0; i < typename.length; i++) {
        data_dict.push({value: data[i], name: typename[i]});
    }
    var chart = echarts.init($("#chart")[0]);
    var option = {
        tooltip: {
            trigger: 'item',
            formatter: "{b} : {c} ({d}%)"
        },
        legend: {
            bottom: 10,
            left: 'center',
            data: typename
        },
        series : [
            {
                type: 'pie',
                radius : '65%',
                center: ['50%', '50%'],
                selectedMode: 'single',
                data: data_dict,
                itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                    }
                }
            }
        ]
    };
    chart.setOption(option);
})

$(window).resize(function () {
    echarts.init($("#chart")[0]).resize();
})
