document.addEventListener("DOMContentLoaded", function () {
    const showAllBtn = document.getElementById("showAllBtn");
    const showLessBtn = document.getElementById("showLessBtn");
  
    /** show all albums or hide albums */
    if (showAllBtn && showLessBtn) {
      showAllBtn.addEventListener("click", function () {
        document.querySelectorAll(".extra-vinyl").forEach(v => {
          v.classList.remove("d-none");
        });
        showAllBtn.classList.add("d-none");
        showLessBtn.classList.remove("d-none");
      });
  
      showLessBtn.addEventListener("click", function () {
        document.querySelectorAll(".extra-vinyl").forEach(v => {
          v.classList.add("d-none");
        });
        showLessBtn.classList.add("d-none");
        showAllBtn.classList.remove("d-none");
        window.scrollTo({ top: document.getElementById("vinylGrid").offsetTop - 100, behavior: 'smooth' });
      });
    }
  });
  