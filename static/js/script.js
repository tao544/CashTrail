// document.addEventListener("DOMContentLoaded", function() {
//   // Pie Chart
//   const pieCtx = document.getElementById('pieChart').getContext('2d');
//   new Chart(pieCtx, {
//     type: 'pie',
//     data: {
//       labels: ['Food', 'Transport', 'Bills', 'Entertainment'],
//       datasets: [{
//         data: [2000, 1500, 3000, 1000],
//         backgroundColor: ['#4caf50', '#2196f3', '#ff9800', '#9c27b0']
//       }]
//     }
//   });

//   // Bar Chart
//   const barCtx = document.getElementById('barChart').getContext('2d');
//   new Chart(barCtx, {
//     type: 'bar',
//     data: {
//       labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
//       datasets: [{
//         label: 'Spending (₦)',
//         data: [5000, 7000, 4000, 6000, 8000, 3000],
//         backgroundColor: '#2196f3'
//       }]
//     },
//     options: {
//       scales: {
//         y: { beginAtZero: true }
//       }
//     }
//   });
// });

//    // Functions to update charts dynamically
//   function updateCategorySpending(newData) {
//     pieChart.data.datasets[0].data = newData;
//     pieChart.update();
//   }

//   function updateMonthlySpending(newData) {
//     barChart.data.datasets[0].data = newData;
//     barChart.update();
//   }

//   // Example usage: simulate spending updates
//   updateCategorySpending([2000, 1500, 3000, 1000]); // Food, Transport, Bills, Entertainment
//   updateMonthlySpending([5000, 7000, 4000, 6000, 8000, 3000]); // Jan–Jun



function togglePassword() {
    const passwordInput = document.getElementById('passwordInput');
    const passwordIcon = document.getElementById('passwordIcon');

    if (passwordInput.type === 'password') {
        passwordInput.type = 'text';
        passwordIcon.classList.remove('bi-eye');
        passwordIcon.classList.add('bi-eye-slash');
    } else {
        passwordInput.type = 'password';
        passwordIcon.classList.remove('bi-eye-slash');
        passwordIcon.classList.add('bi-eye');
    }
}




// navbar js

document.addEventListener("DOMContentLoaded", function () {

  const navLinks = document.querySelectorAll(".nav-scroll");
  const indicator = document.querySelector(".nav-indicator");

  function moveIndicator(el) {
    if (!el || window.innerWidth <= 991) return;

    const rect = el.getBoundingClientRect();
    const parentRect = el.closest(".navbar-nav").getBoundingClientRect();

    indicator.style.width = rect.width + "px";
    indicator.style.left = (rect.left - parentRect.left) + "px";
  }

  navLinks.forEach(link => {
    link.addEventListener("click", function () {
      navLinks.forEach(l => l.classList.remove("active"));
      this.classList.add("active");
      moveIndicator(this);
    });
  });

  // Set default on load
  const active = document.querySelector(".nav-link.active");
  moveIndicator(active);

});



