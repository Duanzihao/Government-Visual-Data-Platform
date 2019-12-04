var chart = echarts.init(document.getElementById('chart'));
var problemdata_dict = [];
for (var i = 0; i < typename.length; i++) {
    problemdata_dict.push({ value: problemdata[i], name: typename[i] });
}
var option = {
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b}: {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        x: 'left',
        data: typename
    },
    series: [
        {
            name: '结办情况',
            type: 'pie',
            selectedMode: 'single',
            radius: [0, '30%'],

            label: {
                normal: {
                    position: 'inner'
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data: [
                { value: execdata[0], name: '处置中' },
                { value: execdata[1], name: '超期结办' },
                { value: execdata[2], name: '按期结办' }
            ]
        },
        {
            name: '问题类型',
            type: 'pie',
            radius: ['35%', '50%'],
            label: {
                normal: {
                    formatter: '{a|{a}}{abg|}\n{hr|}\n  {b|{b}：}{c}  {per|{d}%}  ',
                    backgroundColor: '#eee',
                    borderColor: '#aaa',
                    borderWidth: 1,
                    borderRadius: 4,
                    // shadowBlur:3,
                    // shadowOffsetX: 2,
                    // shadowOffsetY: 2,
                    // shadowColor: '#999',
                    // padding: [0, 7],
                    rich: {
                        a: {
                            color: '#999',
                            lineHeight: 22,
                            align: 'center'
                        },
                        // abg: {
                        //     backgroundColor: '#333',
                        //     width: '100%',
                        //     align: 'right',
                        //     height: 22,
                        //     borderRadius: [4, 4, 0, 0]
                        // },
                        hr: {
                            borderColor: '#aaa',
                            width: '100%',
                            borderWidth: 0.5,
                            height: 0
                        },
                        b: {
                            fontSize: 10,
                            lineHeight: 25
                        },
                        per: {
                            color: '#eee',
                            backgroundColor: '#334455',
                            padding: [1, 4],
                            borderRadius: 21
                        }
                    }
                }
            },
            data: problemdata_dict
        }
    ]
};
chart.setOption(option);
window.onresize = chart.resize;