/* Parse JSON Data from an element created by django.
  This is how we get data into the page from django for use in javascript */
function parseDjangoJSONDump(dumpid) {
  return JSON.parse(document.getElementById('networth_breakdown_list').textContent);
}

/* Get the colors for filling in data areas. */
function getChartDataBackgroundColors(dataLength) {
  return [
      'rgba(255, 99, 132, 1.0)',
      'rgba(54, 162, 235, 0.2)'
  ];
}

/* Get the colors for borders of data areas in chart */
function getChartDataLineColors(dataLength) {
  return getChartDataBackgroundColors(dataLength);
}

/* Create the account breakdown chart
    Shows the value of accounts compared to the total value as a donut */
function createAccountbreakdownChart(canvasid, chartData) {

  var ctx = document.getElementById(canvasid).getContext('2d');
  var myChart = new Chart(ctx, {
      type: 'pie',
      data: {
          labels: chartData.labels,
          datasets: [{
              label: 'Value',
              data: chartData.data,
              backgroundColor: getChartDataBackgroundColors(chartData.data.length),
              borderColor: getChartDataLineColors(chartData.data.length),
              borderWidth: 1
          }],
      },
      options: {
          responsive: false,
          cutoutPercentage: 50
      }
  });
}
