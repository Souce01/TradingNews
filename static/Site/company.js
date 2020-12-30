const ctx = document.getElementById('chart').getContext('2d');
const production = 'https://tradingnews.herokuapp.com'
const local = '127.0.0.1:8000'


// creating the chart with dummy data
let myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: ['one'],
        datasets: [{
            label: 'price',
            data: [0],
            pointRadius: 0
        }]
    },
    options: {
        responsive: true,
        tooltips: {
            mode: 'index',
            intersect: false,
        },
        legend: {
            display: false
        },
        scales: {
            yAxes: [{
                display: true,
                position: 'right',
                gridLines: {
                    display: false
                }
            }
            ],
            xAxes: [{
                ticks: {
                    display: false,
                },
                gridLines: {
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
    try{
        const symbol = getSymbol();
        const resp = await fetch(`${production}/api/chartData/${symbol}/${interval}`);

        // Throws error if response doesn't have 200 status code
        if (!resp.ok)
            throw new Error(resp);
        
        const data = await resp.json();
        const parsedData = data[`Time Series (${interval})`];
        const labels = Object.keys(parsedData);
        let price = [];

        for (const key of labels)
            price.push(parsedData[key]['4. close']);

        // reverse before return to sort from oldest to newest
        return [labels.reverse(), price.reverse()];
    } catch(err){
        console.error(err);
    }
    
}

// input: object, array
// output: none
// description: takes the chart objects and add data inside chart
function addChartData(chart, data){
    try{
        chart.data.labels = data[0];
        chart.data.datasets[0].data = data[1];

        // turns the background color red if the last price is lower than the first
        // otherwise background color is green
        chart.data.datasets[0].backgroundColor = function () {
            let opacity = 0.7
            if (data[1][data[1].length - 1] < data[1][0]) {
                return `rgba(240, 22, 47, ${opacity})`;
            } else {
                return `rgba(0, 204, 92, ${opacity})`;
            }
        }
        
        chart.update();
    } catch(err){
        console.error(err);
    }
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
    try {
        getChartData(interval).then(data => {
            removeChartData(chart);
            addChartData(chart, data);
        })

        // changes color of the selected interval
        // removes previous color of all buttons
        $(".profile-chart-button").removeClass("profile-chart-button-active");

        // Changes color of current button to show that it's selected
        element.addClass("profile-chart-button-active");
    } catch (err) {
        console.error(err);
    }
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
    .on("click", function () {
        updateChart(myChart, '5min', $(this));
    });

$("#profile-chart-button-15m")
    .on("click", function () {
        updateChart(myChart, '15min', $(this));
    });

$("#profile-chart-button-30m")
    .on("click", function () {
        updateChart(myChart, '30min', $(this));
    });

$("#profile-chart-button-60m")
    .on("click", function () {
        updateChart(myChart, '60min', $(this));
    });

// changes text inside the follow button on hover
$(document).on('mouseenter', '.followed', function () {
    $("#follow-button").text("unfollow");
})

$(document).on('mouseleave', '.followed', function () {
    $("#follow-button").text("followed");
})

