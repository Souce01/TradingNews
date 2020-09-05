
initiateChart();
async function initiateChart(){
  const data = await getChartData('IBM', '15min');
  const ctx = document.getElementById('chart').getContext('2d');

  const myChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: data[0],
      datasets: [{
        label: 'price',
        data: data[1],
        pointRadius: 2,
        backgroundColor: function(context){
          if (data[1][data[1].length - 1] < data[1][0]) {
            return 'rgba(240, 22, 47, 0.6)';
          } else {
            return 'rgba(0, 204, 92, 0.6)';
          }
        }
      }]
    },
    options: {
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
}

async function getChartData(symbol, interval){
  const response = await fetch(`http://127.0.0.1:8000/api/chartData/${symbol}/${interval}`)
  const data = await response.json();
  const parsedData = data[`Time Series (${interval})`];
  const labels = Object.keys(parsedData);
  const price = [];

  for (const key of labels) {
    price.push(parsedData[key]['4. close']);
  };

  return [labels.reverse(), price.reverse()];
}


/* Event handlers */

// removes images that didn't load
$(".article-img")
  .on("error", function(e) {
    $(this).remove();
    e.preventDefault();
  })

// Changes the color an article's title on hover
$(".article")
  .hover(function (e){
    $(this).find(".article-title").css("color", "#4193c6");
    e.preventDefault();
  }, function(e){
    $(this).find(".article-title").css("color", "white");
    e.preventDefault();
  })

// makes an api call to get search endpoint
$("#search-field").change(function (e) { 

  e.preventDefault();
});
