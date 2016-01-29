function RealtimeChart(div, name, main_label, xlabel, ylabel, json_src) {
    var chart = new Highcharts.Chart({
        chart: {
            renderTo: div,
            defaultSeriesType: 'spline',
            events: {
                load: ajax_request
            }
        },
        title: {
            text: main_label
        },
        xAxis: {
            type: 'datetime',
            tickPixelInterval: 150,
            maxZoom: 20 * 1000,
            title: {
                text: xlabel
            }
        },
        yAxis: {
            minPadding: 0.2,
            maxPadding: 0.2,
            title: {
                text: ylabel
            }
        },
        tooltip: {
            formatter: function() {
                return '<b>' + this.series.name + '</b><br/>' + Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) + '<br/>' + Highcharts.numberFormat(this.y, 2);
            }
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: {
                        x1: 0,
                        y1: 0,
                        x2: 0,
                        y2: 1
                    },
                    stops: [
                        [0, Highcharts.getOptions().colors[0]],
                        [1, Highcharts.Color(Highcharts.getOptions().colors[0]).
                            setOpacity(0).
                            get('rgba')
                        ]
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },
        series: [{
            type: 'area',
            name: name,
            data: []
        }],
    });

    function ajax_request() {
        $.ajax({
            url: json_src,
            success: function(data) {
                var shift, series;
                var x, y;
                series = chart.series[0];
                shift = series.data.length > 20;
                x = (new Date()).getTime();
                y = data[name];
                series.addPoint([x, y], true, shift);
                setTimeout(ajax_request, 3000);
            },
            cache: false
        });
    }
}

function get_charts(url) {
    cpu_chart = new RealtimeChart(
        'cpu_div',
        'cpu_usage',
        'CPU Load',
        'Snapshot Time',
        'CPU Usage / 100',
        url);
    mem_chart = new RealtimeChart(
        'mem_div',
        'memory_usage',
        'Memory Load',
        'Snapshot Time',
        'Mem / 100',
        url);
}

function get_service_charts(url) {
    bytes_recv_chart = new RealtimeChart(
        'bytes_sent_div',
        'bytes_recv',
        'Received Bytes',
        'Snapshot Time',
        'Bytes',
        url);
    bytes_sent_chart = new RealtimeChart('bytes_recv_div', 'bytes_sent', 'Sent Bytes', 'Snapshot Time', 'Bytes', url);
    requests_chart = new RealtimeChart('requests_div', 'n_requests', 'Number of requests', 'Snapshot Time', 'Requests', url);
    failures_chart = new RealtimeChart('failures_div', 'n_failures', 'Number of failed requests', 'Snapshot Time', 'Requests', url);
    mem_read_chart = new RealtimeChart('mem_read_div', 'shm_reads', 'Shared Memory Reads', 'Snapshot Time', 'Bytes', url);
    mem_wrt_chart = new RealtimeChart('mem_wrt_div', 'shm_writes', 'Shared Memory Writes', 'Snapshot Time', 'Bytes', url);
}
