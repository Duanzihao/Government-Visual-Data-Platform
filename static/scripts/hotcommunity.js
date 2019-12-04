var chart = echarts.init(document.getElementById('chart'))

var data_dict = [];
var sum = 0;
for (var i = 0; i < street.length; i++) {
    data_dict.push({name: street[i], value: data[i]});
    sum += data[i];
}

var geoCoordMap = {
    '碧玲社区': [114.295663,22.67342],
    '和平社区': [114.352397,22.69518],
    '江岭社区': [114.362596,22.69202],
    '金龟社区': [114.406461,22.663744],
    '金沙社区': [114.40542,22.753966],
    '坑梓社区': [114.390013,22.753031],
    '老坑社区': [114.369312,22.734866],
    '六和社区': [114.345313,22.699244],
    '六联社区': [114.332971,22.795219],
    '龙田社区': [114.372841,22.753346],
    '马峦社区': [114.338203,22.644538],
    '南布社区': [114.375607,22.70534],
    '坪环社区': [114.35474,22.688096],
    '坪山社区': [114.357265,22.696259],
    '沙湖社区': [114.331597,22.683988],
    '沙坣社区': [114.377888,22.690889],
    '沙田社区': [114.403344,22.761827],
    '石井社区': [114.391434,22.698242],
    '汤坑社区': [114.331079,22.678805],
    '田头社区': [114.410837,22.697197],
    '田心社区': [114.42088,22.700788],
    '秀新社区': [114.381223,22.746873],
    '竹坑社区': [114.390699,22.717126]
};

var convertData = function (data) {
    var res = [];
    for (var i = 0; i < data.length; i++) {
        var geoCoord = geoCoordMap[data[i].name];
        if (geoCoord) {
            res.push({
                name: data[i].name,
                value: geoCoord.concat(data[i].value)
            });
        }
    }
    return res;
};

function renderItem(params, api) {
    var points = [];
    var color = api.visual('color');

    return {
        type: 'polygon',
        shape: {
            points: echarts.graphic.clipPointsByRect(points, {
                x: params.coordSys.x,
                y: params.coordSys.y,
                width: params.coordSys.width,
                height: params.coordSys.height
            })
        },
        style: api.style({
            fill: color,
            stroke: echarts.color.lift(color)
        })
    };
}

var option = {
    backgroundColor: 'transparent',
    tooltip : {
        trigger: 'item',
        formatter: (p)=>{
            return p.data.name + ": " + p.data.value[2]
        }
    },
    bmap: {
        center: [114.357265,22.696259],
        zoom: 13,
        roam: true,
        mapStyle: {
            styleJson: [
                {
                    "featureType": "water",
                    "elementType": "all",
                    "stylers": {
                        "color": "#044161"
                    }
                },
                {
                    "featureType": "land",
                    "elementType": "all",
                    "stylers": {
                        "color": "#004981"
                    }
                },
                {
                    "featureType": "boundary",
                    "elementType": "geometry",
                    "stylers": {
                        "color": "#064f85"
                    }
                },
                {
                    "featureType": "railway",
                    "elementType": "all",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "highway",
                    "elementType": "geometry",
                    "stylers": {
                        "color": "#004981"
                    }
                },
                {
                    "featureType": "highway",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "color": "#005b96",
                        "lightness": 1
                    }
                },
                {
                    "featureType": "highway",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "arterial",
                    "elementType": "geometry",
                    "stylers": {
                        "color": "#004981"
                    }
                },
                {
                    "featureType": "arterial",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "color": "#00508b"
                    }
                },
                {
                    "featureType": "poi",
                    "elementType": "all",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "green",
                    "elementType": "all",
                    "stylers": {
                        "color": "#056197",
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "subway",
                    "elementType": "all",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "manmade",
                    "elementType": "all",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "local",
                    "elementType": "all",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "arterial",
                    "elementType": "labels",
                    "stylers": {
                        "visibility": "off"
                    }
                },
                {
                    "featureType": "boundary",
                    "elementType": "geometry.fill",
                    "stylers": {
                        "color": "#029fd4"
                    }
                },
                {
                    "featureType": "building",
                    "elementType": "all",
                    "stylers": {
                        "color": "#1a5787"
                    }
                },
                {
                    "featureType": "label",
                    "elementType": "all",
                    "stylers": {
                        "visibility": "off"
                    }
                }
            ]
        }
    },
    series : [
        {

            type: 'scatter',
            coordinateSystem: 'bmap',
            data: convertData(data_dict),
            symbolSize: function (val) {
                return val[2] / (sum / 500);
            },
            label: {
                normal: {
                    formatter: '{b}',
                    position: 'right',
                    show: true
                },
                emphasis: {
                    show: true
                }
            },
            itemStyle: {
                normal: {
                    color: '#f4e925',
                    shadowBlur: 10,
                    shadowColor: '#333'
                }
            }
        },
        {
            type: 'custom',
            coordinateSystem: 'bmap',
            renderItem: renderItem,
            itemStyle: {
                normal: {
                    opacity: 0.5
                }
            },
            animation: false,
            silent: true,
            data: [0],
            z: -10
        }
    ]
};

chart.setOption(option);

var bmap = chart.getModel().getComponent('bmap').getBMap();
bmap.addControl(new BMap.MapTypeControl());