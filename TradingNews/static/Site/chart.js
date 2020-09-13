const ctx = document.getElementById('chart').getContext('2d');

// creating the chart with dummy data
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
updateChart(myChart, '5min', $("#profile-chart-button-5m"));


/* CHART FUNCTIONS */

// input: string
// output: array
// description: fetch chart labels and chart data from the back-end
async function getChartData(interval) {
    try {
        const symbol = getSymbol();
        const resp = await fetch(`http://127.0.0.1:8000/api/chartData/${symbol}/${interval}`);

        // Throws error if response doesn't have 200 status code
        if (!resp.ok) throw Error(resp.statusText);

        const data = await resp.json();
        const parsedData = data[`Time Series (${interval})`];
        const labels = Object.keys(parsedData);
        let price = [];

        for (const key of labels) {
            price.push(parsedData[key]['4. close']);
        };

        // reverse before return to sort from oldest to newest
        return [labels.reverse(), price.reverse()];
    } catch (err) {
        console.log(err);
    }
}

// input: object, array
// output: none
// description: takes the chart objects and add data inside chart
function addChartData(chart, data){
    chart.data.labels = data[0];
    chart.data.datasets[0].data = data[1];

    // turns the background color red if the last price is lower than the first
    // otherwise background color is green
    chart.data.datasets[0].backgroundColor = function () {
        if (data[1][data[1].length - 1] < data[1][0]) {
            return 'rgba(240, 22, 47, 0.6)';
        } else {
            return 'rgba(0, 204, 92, 0.6)';
        }
    }
    
    chart.update();
}

// input: object
// output: none
// description: removes labels and data from the chart object
function removeChartData(chart){
    chart.data.labels.pop();
    chart.data.datasets.forEach((dataset) => {
        dataset.data.pop();
    });
    chart.update();
}

// input: object, string, DOM element
// output: none
// description: 
//  -updates the chart with the data from getChartData
//  -adds a css class to the button element related to the selected interval
function updateChart(chart, interval, element){
    getChartData(interval).then(data =>{
        removeChartData(chart);
        addChartData(chart, data);
    })

    // changes color of the selected interval
    // removes previous color of all buttons
    $(".profile-chart-button").removeClass("profile-chart-button-active");

    // Changes color of current button to show that it's selected
    element.addClass("profile-chart-button-active");
}

// input: none
// output: string
// description: get the company symbol of current page
function getSymbol() {
    let url = window.location.pathname.split("/");
    return url[2];
}

/* CHART HANDLERS */
$("#profile-chart-button-5m")
    .on("click", function (e) {
        updateChart(myChart, '5min', $(this));
        e.preventDefault();
    });

$("#profile-chart-button-15m")
    .on("click", function (e) {
        updateChart(myChart, '15min', $(this));
        e.preventDefault();
    });

$("#profile-chart-button-30m")
    .on("click", function (e) {
        updateChart(myChart, '30min', $(this));
        e.preventDefault();
    });

$("#profile-chart-button-60m")
    .on("click", function (e) {
        updateChart(myChart, '60min', $(this));
        e.preventDefault();
    });