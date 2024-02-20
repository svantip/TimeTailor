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

  let isEditMode = false;

  const quickAddEditToggle = document.getElementById("quickaddedit-toggle");
  const quickAddEditIcon = document.getElementById("quickaddediticon");
  assignEventListenersToStarttimeToggles();

  if (quickAddEditToggle && quickAddEditIcon) {
    quickAddEditToggle.addEventListener("click", function (event) {
      event.preventDefault(); 
      isEditMode = !isEditMode; 

      const plusIcons = document.querySelectorAll(".bxs-plus-circle");
      plusIcons.forEach(function (icon) {
        if (isEditMode) {
          icon.classList.add("edit");
        } else {
          icon.classList.remove("edit");
        }
      });
      if (isEditMode) {
        quickAddEditIcon.classList.remove("bx-edit-alt");
        quickAddEditIcon.classList.add("bxs-edit-alt");
      } else {
        quickAddEditIcon.classList.add("bx-edit-alt");
        quickAddEditIcon.classList.remove("bxs-edit-alt");
      }
      assignEventListenersToStarttimeToggles();
    });
  } else {
    console.error("Element not found");
  }

  function assignEventListenersToStarttimeToggles() {
    const starttimeToggles = document.querySelectorAll(".starttime-toggle");
    starttimeToggles.forEach(function (starttimeToggle) {
      
      starttimeToggle.removeEventListener("click", handleStarttimeToggleClick);
      starttimeToggle.removeEventListener("click", handleStarttimeToggleDelete);

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
    console.log('Attempting to delete task with ID:', taskId); 
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
    event.preventDefault();
  
    assignEventListenersToStarttimeToggles();
  });

  quickAddToggle.addEventListener("click", function (event) {
    event.preventDefault(); 
    quickAddFormContainer.style.display = "block";
    backdrop.style.display = "block";
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

    event.preventDefault(); 
    taskAddForm.style.display = "block";
    backdrop3.style.display = "block"; 
  });
  
  if (closeModal) {
    closeModal.addEventListener("click", function () {
      quickAddFormContainer.style.display = "none";
      backdrop.style.display = "none";
    });
  }
 
  if (closeModal2) {
    closeModal2.addEventListener("click", function () {
      starttimeFormContainer.style.display = "none";
      backdrop2.style.display = "none";
    });
  }
  
  if (closeModal3) {
    closeModal3.addEventListener("click", function () {
      taskAddForm.style.display = "none";
      backdrop3.style.display = "none";
    });
  }
});
