document.addEventListener("DOMContentLoaded", function() {
  // Pie Chart
  const pieCtx = document.getElementById('pieChart').getContext('2d');
  new Chart(pieCtx, {
    type: 'pie',
    data: {
      labels: ['Food', 'Transport', 'Bills', 'Entertainment'],
      datasets: [{
        data: [2000, 1500, 3000, 1000],
        backgroundColor: ['#4caf50', '#2196f3', '#ff9800', '#9c27b0']
      }]
    }
  });

  // Bar Chart
  const barCtx = document.getElementById('barChart').getContext('2d');
  new Chart(barCtx, {
    type: 'bar',
    data: {
      labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
      datasets: [{
        label: 'Spending (₦)',
        data: [5000, 7000, 4000, 6000, 8000, 3000],
        backgroundColor: '#2196f3'
      }]
    },
    options: {
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
});

   // Functions to update charts dynamically
  function updateCategorySpending(newData) {
    pieChart.data.datasets[0].data = newData;
    pieChart.update();
  }

  function updateMonthlySpending(newData) {
    barChart.data.datasets[0].data = newData;
    barChart.update();
  }

  // Example usage: simulate spending updates
  updateCategorySpending([2000, 1500, 3000, 1000]); // Food, Transport, Bills, Entertainment
  updateMonthlySpending([5000, 7000, 4000, 6000, 8000, 3000]); // Jan–Jun

