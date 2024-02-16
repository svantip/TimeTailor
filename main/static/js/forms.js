document.addEventListener("DOMContentLoaded", function () {
    
    
    var toggleButton = document.querySelector(".sidebar-toggle");
    var sidebar = document.querySelector(".sidebar");


    var quickAddToggle = document.getElementById("quickadd-toggle");
    var quickAddFormContainer = document.querySelector(".quickadd-form");
    var backdrop = document.getElementById("backdrop");
    var closeModal = document.getElementById("close-modal");

    var starttimeToggles = document.querySelectorAll(".starttime-toggle");
    var starttimeFormContainer = document.getElementById("starttime-form-container");
    var backdrop2 = document.getElementById("backdrop2");
    var closeModal2 = document.getElementById("close-modal2");

    toggleButton.addEventListener("click", function () {
      sidebar.classList.toggle("active");
    });

    starttimeToggles.forEach(function(starttimeToggle) {
      starttimeToggle.addEventListener("click", function(event) {
          event.preventDefault(); // Prevent the default anchor behavior

          var taskName = this.getAttribute('data-name');
          var taskIcon = this.getAttribute('data-icon');
          var taskColor = this.getAttribute('data-color');
          var taskDuration = this.getAttribute('data-duration');

          document.getElementById('taskName').value = taskName;
          document.getElementById('taskIcon').value = taskIcon;
          document.getElementById('taskColor').value = taskColor;
          document.getElementById('taskDuration').value = taskDuration;

          starttimeFormContainer.style.display = "block";
          backdrop.style.display = "block"; // Show backdrop when form is displayed
      });
  });

    quickAddToggle.addEventListener("click", function (event) {
      event.preventDefault(); // Prevent the default anchor behavior
      quickAddFormContainer.style.display = "block";
      backdrop.style.display = "block"; // Show backdrop when form is displayed
    });

    // Optional: Close the modal when the backdrop is clicked
    if (backdrop) {
      backdrop.addEventListener("click", function () {
        quickAddFormContainer.style.display = "none";
        backdrop.style.display = "none"; // Hide backdrop
      });
    }

    // Optional: Close the modal when the close button is clicked
    if (closeModal) {
      closeModal.addEventListener("click", function () {
        quickAddFormContainer.style.display = "none";
        backdrop.style.display = "none";
      });
    }
    if (backdrop2) {
      backdrop2.addEventListener("click", function () {
        starttimeFormContainer.style.display = "none";
        backdrop2.style.display = "none"; // Hide backdrop
      });
    }

    // Optional: Close the modal when the close button is clicked
    if (closeModal2) {
      closeModal2.addEventListener("click", function () {
        starttimeFormContainer.style.display = "none";
        backdrop2.style.display = "none";
      });
    }
  });