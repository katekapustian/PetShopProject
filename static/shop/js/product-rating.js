document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.product-rating label');
    const ratingValueDisplay = document.getElementById('rating-value');

    stars.forEach(star => {
        star.addEventListener('click', function () {
            const rating = this.getAttribute('data-value');
            stars.forEach((s, index) => {
                s.querySelector('i.ti-star').style.color = index < rating ? '#7e4c4f' : '#ccc';
            });
            ratingValueDisplay.textContent = `(${rating})`;
        });

        star.addEventListener('mouseover', function () {
            const hoverValue = this.getAttribute('data-value');
            stars.forEach((s, index) => {
                s.querySelector('i.ti-star').style.color = index < hoverValue ? '#7e4c4f' : '#ccc';
            });
        });

        star.addEventListener('mouseout', function () {
            const selectedRating = document.querySelector('input[name="rating"]:checked');
            const rating = selectedRating ? selectedRating.value : 0;
            stars.forEach((s, index) => {
                s.querySelector('i.ti-star').style.color = index < rating ? '#7e4c4f' : '#ccc';
            });
        });
    });
});
