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


// childlogin toggle password

function togglepin() {
  const passwordInput = document.getElementById("password");
  const icon = event.target.closest("span").querySelector("i");

  if (passwordInput.type === "password") {
    passwordInput.type = "text";
    icon.classList.remove("fa-eye");
    icon.classList.add("fa-eye-slash");
  } else {
    passwordInput.type = "password";
    icon.classList.remove("fa-eye-slash");
    icon.classList.add("fa-eye");
  }
}



