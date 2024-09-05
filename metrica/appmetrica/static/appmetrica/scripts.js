// global chart object, only used in 'metric.html'
let metricChart;

// data for said chart object
// stored outside of metricChart for ease of access
// changing data here will impact the graph directly
let chartData = {
    keys: [],
    values: [],
    ids: []
};

// an entry marked for deletion/edit
let targetValue = {
    timestamp: "",
    value: "",
    id: "",
    idx: ""
}

// button redirect
function redirectto(url) {
    window.location.href = url;
}

// back button redirect
function redirectback(url) {
    window.history.back();
    // window.location.replace(url);
}

function buildAGraph(metricdata, metricname) {
    let ctx = document.getElementById("metric-graph");
    chartData.keys = Array(metricdata.length);
    chartData.values = Array(metricdata.length);
    chartData.ids = Array(metricdata.length);

    for (let i = 0; i < metricdata.length; i++) {
        chartData.keys[i] = metricdata[i]["key"];
        chartData.values[i] = metricdata[i]["value"];
        chartData.ids[i] = metricdata[i]["id"];
    }

    metricChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: chartData.keys,
            datasets: [
                {
                    label: metricname,
                    data: chartData.values,
                    fill: false
                }
            ]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            onClick: function(evt) {
                var element = metricChart.getElementsAtEventForMode(evt, 'nearest', { intersect: true }, true);
                if (element.length > 0) {
                    var idx = element[0].index;
                    targetValue.id = chartData.ids[idx];
                    targetValue.timestamp = chartData.keys[idx];
                    targetValue.value = chartData.values[idx];
                    targetValue.idx = idx;
                    togglePopup("del-base");
                }
            },
            plugins: {
                tooltip: {
                    enabled: false,
                    external: function(context) {
                        let tooltipEl = document.getElementById('chartjs-tooltip');

                        // Create element on first render
                        if (!tooltipEl) {
                            tooltipEl = document.createElement('div');
                            tooltipEl.id = 'chartjs-tooltip';
                            document.body.appendChild(tooltipEl);
                            tooltipEl.innerHTML = "<table class=\"tt-wrapper\"><thead></thead><tbody></tbody></table>"
                        }

                        // Hide if no tooltip
                        const tooltipModel = context.tooltip;
                        if (tooltipModel.opacity === 0) {
                            tooltipEl.style.opacity = 0;
                            return;
                        }

                        // Set caret Position
                        tooltipEl.classList.remove('above', 'below', 'no-transform');
                        if (tooltipModel.yAlign) {
                            tooltipEl.classList.add(tooltipModel.yAlign);
                        } else {
                            tooltipEl.classList.add('no-transform');
                        }

                        // Set Text
                        if (tooltipModel.body) {
                            let thead = tooltipEl.querySelector("thead");
                            let tbody = tooltipEl.querySelector("tbody");
                            thead.innerHTML = "<tr></tr>"
                            tbody.innerHTML = "<tr></tr><tr></tr>"
                            let valRow = document.createElement("th");
                            valRow.innerHTML = "Value: " + chartData.values[metricChart.tooltip.dataPoints[0].dataIndex];
                            
                            let tsRow = document.createElement("td");
                            tsRow.innerHTML = "Timestamp: " + chartData.keys[metricChart.tooltip.dataPoints[0].dataIndex];

                            let idRow = document.createElement("td");
                            idRow.innerHTML = "ID: " + chartData.ids[metricChart.tooltip.dataPoints[0].dataIndex];

                            thead.children[0].appendChild(valRow);
                            tbody.children[0].appendChild(tsRow);
                            tbody.children[1].appendChild(idRow);
                        }

                        const position = context.chart.canvas.getBoundingClientRect();
                        const bodyFont = Chart.helpers.toFont(tooltipModel.options.bodyFont);

                        // Display, position, and set styles for font
                        tooltipEl.style.opacity = 1;
                        tooltipEl.style.position = 'absolute';
                        tooltipEl.style.left = position.left + window.pageXOffset + tooltipModel.caretX + 'px';
                        tooltipEl.style.top = position.top + window.pageYOffset + tooltipModel.caretY + 'px';
                        tooltipEl.style.font = bodyFont.string;
                        tooltipEl.style.padding = tooltipModel.padding + 'px ' + tooltipModel.padding + 'px';
                        tooltipEl.style.pointerEvents = 'none';
                    }
                }
            }
        }
    });
}

async function deleteMetricValue(url) {
    var data = {
        mvid: targetValue.id
    }

    var rspns = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data)
    });

    var res = await rspns.text();
    chartData.keys.splice(targetValue.idx, 1);
    chartData.values.splice(targetValue.idx, 1);
    chartData.ids.splice(targetValue.idx, 1);
    metricChart.update();
    togglePopup('del-base');
}

function markForDeletion(btn) {
    targetValue.id = btn.dataset.pid;
    togglePopup('del-base');
}

function togglePopup(divid) {
    var wndw = document.getElementById(divid);
    if (wndw.style.display == "flex") {
        wndw.style.display = "none";
    }
    else {
        wndw.style.display = "flex";
    }
}

async function addMetricValue(url) {
    var mid = document.getElementById("ppp-infobox").dataset.mid;
    var ts = document.getElementById('addl-timestamp').value;
    var val = document.getElementById('addl-value').value;

    var data = {
        "metric": mid,
        "timestamp": ts,
        "value": val
    }

    // console.log(data);

    var result = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data),
    });
    // console.log(result);

    result = await result.json();
    // console.log(metricChart);
    if (result.res == "OK") {
        var ll = metricChart.config.data.datasets[0].data.length;
        var i = 0;
        var updateFlag = false;
        // todo: binsearch optimisation
        for (; i < ll; i++) {
            if (ts - metricChart.config.data.labels[i] >= 0) continue;
            // metricChart.config.data.datasets[0].data.splice(i, 0, val);
            chartData.values.splice(i, 0, val);
            // metricChart.config.data.labels.splice(i, 0, ts);
            chartData.keys.splice(i, 0, ts);
            chartData.ids.splice(i, 0, result.id);
            updateFlag = true;
            break;
        }
        if (!updateFlag) {
            chartData.values.push(val);
            chartData.keys.push(ts);
            chartData.ids.push(result.id);
        }
        metricChart.update();
    }

    togglePopup('addl-base');
}

async function addProduct(url, prodflag) {
    var newName = document.getElementById("addl-name").value;
    var data = {};
    if (prodflag == "true") {
        data = {
            "prod-name": newName
        };
    }
    else {
        data = {
            "metr-name": newName,
            "prod-id": document.querySelector("body").dataset.pid
        };
    }

    var res = await fetch(url, {
        method: "POST",
        body: JSON.stringify(data)
    });

    res = await res.json();
    // console.log(res);

    window.location.reload();
}

async function delProduct(delurl, prodflag) {
    var data = {}
    if (prodflag) {
        data = {
            "pid": targetValue.id
        };
    }
    else {
        data = {
            "mid": targetValue.id
        }
    }

    var res = await fetch(delurl, {
        method: "POST",
        body: JSON.stringify(data)
    });

    res = await res.text();
    
    var divToRemove = document.getElementById(targetValue.id);
    if (divToRemove.nextElementSibling != null) {
        divToRemove.nextElementSibling.remove();
    }
    else if(divToRemove.previousElementSibling != null) {
        divToRemove.previousElementSibling.remove();
    }
    divToRemove.remove();
    togglePopup('del-base');
}