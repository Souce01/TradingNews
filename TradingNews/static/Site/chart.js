const ctx = document.getElementById('chart').getContext('2d');
let myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['1'],
        datasets: [{
            label: 'price',
            data: [1],
            pointRadius: 2
        }]
    },
    options: {
        responsive: true,
        legend: {
            display: false
        },
        scales: {
            xAxes: [{
                ticks: {
                    display: false
                }
            }]
        }
    }
});

console.log(myChart.data.labels);

function initiateChart(chart, interval){
    console.log('inside initiate data');
    getChartData(interval).then(data => {
        console.log('inside initiate data');
        console.log(chart.data.labels);
        removeChartData(chart);
        console.log(chart.data.labels);
        addChartData(chart, data);
        console.log(chart.data.labels);
    })
    chart.update();
}

function addChartData(chart, data){
    chart.data.labels.push(data[0]);
    chart.data.datasets.forEach((dataset) => {
        dataset.data.push(data[1]);
        dataset.backgroundColor = function () {
            if (data[1][data[1].length - 1] < data[1][0]) {
                return 'rgba(240, 22, 47, 0.6)';
            } else {
                return 'rgba(0, 204, 92, 0.6)';
            }
        }
    });
    chart.update();
}

function removeChartData(chart){
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}

function updateChart(chart, interval){
    getChartData(interval).then(data =>{
        removeChartData(chart);
        addChartData(chart, data);
    })
}

async function getChartData(interval) {
    const symbol = getSymbol();
    const response = await fetch(`http://127.0.0.1:8000/api/chartData/${symbol}/${interval}`)
    const data = await response.json();
    const parsedData = data[`Time Series (${interval})`];
    const labels = Object.keys(parsedData);
    let price = [];

    for (const key of labels) {
        price.push(parsedData[key]['4. close']);
    };

    // reverse before return to sort from oldest to newest
    return [labels.reverse(), price.reverse()];
}

// returns the symbol of the current company page
function getSymbol() {
    let url = window.location.pathname.split("/");
    return url[2];
}


/* chart handlers */
$("#profile-chart-button-5m")
    .on("click", function (e) {
        updateChart(myChart, '5min');
    });

$("#profile-chart-button-15m")
    .on("click", function (e) {
        updateChart(myChart, '15min');
    });

$("#profile-chart-button-30m")
    .on("click", function (e) {
        updateChart(myChart, '30min');
    });

$("#profile-chart-button-60m")
    .on("click", function (e) {
        updateChart(myChart, '60min');
    });