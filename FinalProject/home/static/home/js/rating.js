document.addEventListener("DOMContentLoaded", function () {
    const stars = document.querySelectorAll(".rate-star");
    const ratingContainer = document.getElementById("rating-stars");
    const favBtn = document.getElementById("fav-btn");
    const vinylId = ratingContainer?.dataset.vinylId;
    const csrfToken = ratingContainer?.dataset.csrf;
  
    /** highlight each star */
    function highlightStars(value) {
        stars.forEach(star => {
            const v = parseInt(star.dataset.value);
            star.classList.remove("fa-star", "fa-star-o");
            star.classList.add(v <= value ? "fa-star" : "fa-star-o");
        });
    }
  
    stars.forEach(star => {
        star.addEventListener("click", function () {
            const value = this.dataset.value;
  
        /** send rating to backend */
            fetch(`/rate/${vinylId}/`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": csrfToken,
                    "Content-Type": "application/x-www-form-urlencoded"
                },
                body: `stars=${value}`
            })
            .then(res => res.json())
            .then(data => {
                highlightStars(value);

            /** update average rating */
                document.querySelector(".text-muted strong").innerText = data.average.toFixed(1);
                document.querySelector(".text-muted").innerHTML =
                `Average Rating: <strong>${data.average.toFixed(1)}</strong> ★ (${data.total} rating${data.total !== 1 ? 's' : ''})`;
            });
        });
    });
  
    favBtn?.addEventListener("click", () => {
        const icon = favBtn.querySelector("i");
        const countSpan = favBtn.querySelector("span");
  
        /** send favorite request to backend */
        fetch(`/favorite/${favBtn.dataset.vinylId}/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": favBtn.dataset.csrf
            }
        })
            .then(res => res.json())
            .then(data => {
                /** update count */
                    if (data.favorited) {
                        icon.classList.remove("fa-heart-o");
                        icon.classList.add("fa-heart", "text-danger");
                    } else {
                        icon.classList.remove("fa-heart", "text-danger");
                        icon.classList.add("fa-heart-o");
                    }
                    countSpan.textContent = data.total;
            });
    });
});
  