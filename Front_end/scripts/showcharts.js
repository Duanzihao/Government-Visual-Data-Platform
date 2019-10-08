// show chart1
var chart1 = echarts.init(document.getElementById('chart1'));
var optionOfChart1 = {
    tooltip : {
        trigger: 'axis',
        axisPointer : {            // 坐标轴指示器，坐标轴触发有效
            type : 'shadow'        // 默认为直线，可选为：'line' | 'shadow'
        }
    },
    legend: {
        data: ['安全隐患','党纪政纪','党建群团','规土城建','环保水务','交通运输','教育卫生','劳动社保','民政服务','社区管理','医药市监']
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis:  {
        type: 'value'
    },
    yAxis: {
        type: 'category',
        data: ['碧玲街道','坑梓街道','龙田街道','马峦街道','坪山街道','石井街道']
    },
    series: [
        {
            name: '安全隐患',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [32, 30, 30, 33, 39, 33]
        },
        {
            name: '党纪政纪',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [12, 13, 10, 13, 9, 23]
        },
        {
            name: '党建群团',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [22, 18, 19, 23, 29, 33]
        },
        {
            name: '规土城建',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [15, 21, 20, 15, 19, 33]
        },
        {
            name: '环保水务',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [16, 16, 18, 18, 24, 21]
        },
        {
            name: '交通运输',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [12, 15, 18, 14, 13, 17]
        },
        {
            name: '教育卫生',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [21, 14, 28, 27, 30, 18]
        },
        {
            name: '劳动社保',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [13, 29, 25, 24, 17, 19]
        },
        {
            name: '民政服务',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [17, 19, 15, 10, 18, 11]
        },
        {
            name: '社区管理',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [33, 24, 35, 21, 25, 14]
        },
        {
            name: '医药市监',
            type: 'bar',
            stack: '总量',
            label: {
                normal: {
                    show: true,
                    position: 'insideRight'
                }
            },
            data: [12, 10, 18, 15, 17, 11]
        }
    ]
};
chart1.setOption(optionOfChart1);

// show chart2
var chart2 = echarts.init(document.getElementById('chart2'))
var optionOfChart2 = {
    legend: {
        // orient: 'vertical',
        // top: 'middle',
        bottom: 10,
        left: 'center',
        data: ['投诉','感谢','建议','求决','咨询','其他']
    },
    series : [
        {
            type: 'pie',
            radius : '65%',
            center: ['50%', '50%'],
            selectedMode: 'single',
            data:[
                {value:20, name: '投诉'},
                {value:17, name: '感谢'},
                {value:9, name: '建议'},
                {value:3, name: '求决'},
                {value:7, name: '咨询'},
                {value:6, name: '其他'}
            ],
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

chart2.setOption(optionOfChart2)
