document.addEventListener("DOMContentLoaded", function () {
  var toggleButton = document.querySelector(".sidebar-toggle");
  var sidebar = document.querySelector(".sidebar");

  var quickAddToggle = document.getElementById("quickadd-toggle");
  var quickAddFormContainer = document.querySelector(".quickadd-form");
  var backdrop = document.getElementById("backdrop");
  var closeModal = document.getElementById("close-modal");

  var fab = document.getElementById("fab");
  var taskAddForm = document.getElementById("addtask-form-container");
  var backdrop3 = document.getElementById("backdrop3");
  var closeModal3 = document.getElementById("close-modal3");

  var starttimeToggles = document.querySelectorAll(".starttime-toggle");
  var starttimeFormContainer = document.getElementById("starttime-form-container");
  var backdrop2 = document.getElementById("backdrop2");
  var closeModal2 = document.getElementById("close-modal2");

  let isEditMode = false; // Flag to track the edit mode state

  const quickAddEditToggle = document.getElementById("quickaddedit-toggle");
  const quickAddEditIcon = document.getElementById("quickaddediticon");
  assignEventListenersToStarttimeToggles();

  if (quickAddEditToggle && quickAddEditIcon) {
    quickAddEditToggle.addEventListener("click", function (event) {
      event.preventDefault(); // Prevents the default action
      isEditMode = !isEditMode; // Toggle the edit mode state

      const plusIcons = document.querySelectorAll(".bxs-plus-circle");
      plusIcons.forEach(function (icon) {
        if (isEditMode) {
          icon.classList.add("edit");
        } else {
          icon.classList.remove("edit");
        }
      });

      // Correctly toggling icon classes
      if (isEditMode) {
        quickAddEditIcon.classList.remove("bx-edit-alt");
        quickAddEditIcon.classList.add("bxs-edit-alt");
      } else {
        quickAddEditIcon.classList.add("bx-edit-alt");
        quickAddEditIcon.classList.remove("bxs-edit-alt");
      }
      // Reassign event listeners based on mode
      assignEventListenersToStarttimeToggles();
    });
  } else {
    console.error("Element not found");
  }

  function assignEventListenersToStarttimeToggles() {
    const starttimeToggles = document.querySelectorAll(".starttime-toggle");
    starttimeToggles.forEach(function (starttimeToggle) {
      
      // Remove any existing event listener to prevent duplicates
      starttimeToggle.removeEventListener("click", handleStarttimeToggleClick);
      starttimeToggle.removeEventListener("click", handleStarttimeToggleDelete);

      // Add the appropriate event listener based on isEditMode
      if (isEditMode) {
        starttimeToggle.addEventListener("click", handleStarttimeToggleDelete);
      } else {
        starttimeToggle.addEventListener("click", handleStarttimeToggleClick);
      }
    });
  }

  function handleStarttimeToggleClick(event) {
    event.preventDefault();
    console.log('handleStarttimeToggleClick is assigned')
    // This variable should be declared here if it's not globally available
    const starttimeFormContainer = document.getElementById("starttime-form-container");
    const backdrop = document.getElementById("backdrop");

    var taskName = this.getAttribute("data-name");
    var taskIcon = this.getAttribute("data-icon");
    var taskColor = this.getAttribute("data-color");
    var taskDuration = this.getAttribute("data-duration");

    document.getElementById("taskName").value = taskName;
    document.getElementById("taskIcon").value = taskIcon;
    document.getElementById("taskColor").value = taskColor;
    document.getElementById("taskDuration").value = taskDuration;

    starttimeFormContainer.style.display = "block";
    backdrop.style.display = "block";
  }

  function handleStarttimeToggleDelete(event) {
    event.preventDefault();
    console.log('handleStarttimeToggleDelete is assigned')
    const taskId = this.closest('.quickaddcard').getAttribute('data-task-id');
    console.log('Attempting to delete task with ID:', taskId); // Debug line
    if (!taskId) {
      alert("Task ID is missing.");
      return;
    }

    if (confirm("Are you sure you want to delete this task?")) {
      const csrftoken = document.querySelector("[name=csrf-token]").content;
      fetch(`/delete-task/${taskId}/`, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrftoken,
          "Content-Type": "application/json",
        },
      })
        .then((response) => {
          if (response.ok) {
            
            console.log("Task deleted successfully");
            location.reload();
          } else {
            alert("There was an error deleting the task.");
          }
        })
        .catch((error) => console.error("Error:", error));
    }
  }

  quickAddEditToggle.addEventListener("click", function (event) {
    event.preventDefault(); // Prevents the default action
    // Toggle the edit mode state
    assignEventListenersToStarttimeToggles(); // Update event listeners based on the new mode
  });

  quickAddToggle.addEventListener("click", function (event) {
    event.preventDefault(); // Prevent the default action
    quickAddFormContainer.style.display = "block";
    backdrop.style.display = "block"; // Show the backdrop
  });
  fab.addEventListener("click", function (event) {
    document.getElementById("iconInput2").className = null;
    document.getElementById("currentIcon2").className = "bx bxs-coffee";
    document.getElementById("colorIcon2").className = "bx bxs-coffee";
    document.getElementById("color2").value = null;
    document.getElementById("namaewa").value = null;
    document.querySelector('[name="color"]').value = null;
    document.querySelector('[name="duration_hours"]').value = null;
    document.querySelector('[name="duration_minutes"]').value = null;
    document.getElementById("taskadd-id").value = null;
    document.getElementById("submitBtn").innerText = "Add Task";
    document.getElementById("title").innerText = "Add Task";

    event.preventDefault(); // Prevent the default anchor behavior
    taskAddForm.style.display = "block";
    backdrop3.style.display = "block"; // Show backdrop when form is displayed
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

  if (backdrop3) {
    backdrop3.addEventListener("click", function () {
      taskAddForm.style.display = "none";
      backdrop3.style.display = "none"; // Hide backdrop
    });
  }

  // Optional: Close the modal when the close button is clicked
  if (closeModal3) {
    closeModal3.addEventListener("click", function () {
      taskAddForm.style.display = "none";
      backdrop3.style.display = "none";
    });
  }
});
