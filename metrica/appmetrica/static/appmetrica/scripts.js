function sendform(btn) {
    let form_id = btn.dataset.formid;
    let form_name = "form-" + form_id;
    let form = document.getElementsByName(form_name);
    form[0].submit();
}

function redirectto(url) {
    window.location.replace(url);
}

function buildAGraph(metricdata, metricname) {
    let ctx = document.getElementById("metric-graph");
    let keys = Array(metricdata.length);
    let values = Array(metricdata.length);

    for (let i = 0; i < metricdata.length; i++) {
        keys[i] = metricdata[i]["key"];
        values[i] = metricdata[i]["value"];
    }

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: keys,
            datasets: [{
                label: metricname,
                data: values,
                fill: false
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
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
