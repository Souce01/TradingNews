initiateChart();
async function initiateChart() {
    const data = await getChartData('15min');
    const ctx = document.getElementById('chart').getContext('2d');

    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data[0],
            datasets: [{
                label: 'price',
                data: data[1],
                pointRadius: 2,
                backgroundColor: function () {
                    if (data[1][data[1].length - 1] < data[1][0]) {
                        return 'rgba(240, 22, 47, 0.6)';
                    } else {
                        return 'rgba(0, 204, 92, 0.6)';
                    }
                }
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

    let chart = document.getElementById('chart');
}

async function getChartData(interval) {
    const symbol = getSymbol();
    const response = await fetch(`http://127.0.0.1:8000/api/chartData/${symbol}/${interval}`)
    const data = await response.json();
    const parsedData = data[`Time Series (${interval})`];
    const labels = Object.keys(parsedData);
    const price = [];

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
