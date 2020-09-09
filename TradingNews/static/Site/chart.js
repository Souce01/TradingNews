const ctx = document.getElementById('chart').getContext('2d');

// creating the chart with dummy data that won't be displayed
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

// initiate the chart with 5min interval data
updateChart(myChart, '5min');

function addChartData(chart, data){
    chart.data.labels = data[0];
    chart.data.datasets[0].data = data[1];
    chart.data.datasets[0].backgroundColor = function () {
        if (data[1][data[1].length - 1] < data[1][0]) {
            return 'rgba(240, 22, 47, 0.6)';
        } else {
            return 'rgba(0, 204, 92, 0.6)';
        }
    }
    
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
    try{
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
    } catch(err){
        console.log(err);
    }
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

        // removes previous color of all buttons
        $(".profile-chart-button").css("color", "white");
        
        // Changes color of current button to show that it's selected
        $(this).css("color", "#4193c6");
        e.preventDefault();
    });

$("#profile-chart-button-15m")
    .on("click", function (e) {
        updateChart(myChart, '15min');

        // removes previous color of all buttons
        $(".profile-chart-button").css("color", "white");

        // Changes color of current button to show that it's selected
        $(this).css("color", "#4193c6");
        e.preventDefault();
    });

$("#profile-chart-button-30m")
    .on("click", function (e) {
        updateChart(myChart, '30min');

        // removes previous color of all buttons
        $(".profile-chart-button").css("color", "white");

        // Changes color of current button to show that it's selected
        $(this).css("color", "#4193c6");
        e.preventDefault();
    });

$("#profile-chart-button-60m")
    .on("click", function (e) {
        updateChart(myChart, '60min');

        // removes previous color of all buttons
        $(".profile-chart-button").css("color", "white");

        // Changes color of current button to show that it's selected
        $(this).css("color", "#4193c6");
        e.preventDefault();
    });

/*
$(".profile-chart-button")
    .hover(function (e) {
        $(this).css("color", "#4193c6");
        e.preventDefault();
    }, function (e) {
        $(this).css("color", "white");
        e.preventDefault();
    });
*/