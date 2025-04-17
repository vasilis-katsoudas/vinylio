document.addEventListener("DOMContentLoaded", function () {
    const editBtn = document.getElementById("editBtn");
    const saveBtn = document.getElementById("saveBtn");
    const inputs = document.querySelectorAll("#profileForm input");
    const passwordSection = document.getElementById("passwordSection");

    editBtn.addEventListener("click", function () {
      inputs.forEach(input => input.removeAttribute("readonly"));
      passwordSection.classList.remove("d-none");
      editBtn.classList.add("d-none");
      saveBtn.classList.remove("d-none");
    });
  });