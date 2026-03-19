document.addEventListener("DOMContentLoaded", function () {

  const toggleBtn = document.querySelector('.sidebar-toggle');
  const sidebar = document.getElementById('sidebar');
  const overlay = document.getElementById('overlay');

  if (toggleBtn) {

    const toggleIcon = toggleBtn.querySelector('i');

    toggleBtn.addEventListener('click', () => {
      sidebar.classList.toggle('active');
      overlay.classList.toggle('active');

      if (sidebar.classList.contains('active')) {
        toggleIcon.classList.replace('fa-bars', 'fa-times');
      } else {
        toggleIcon.classList.replace('fa-times', 'fa-bars');
      }
    });

    overlay.addEventListener('click', () => {
      sidebar.classList.remove('active');
      overlay.classList.remove('active');
      toggleIcon.classList.replace('fa-times', 'fa-bars');
    });

  }

});



