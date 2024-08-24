document.addEventListener("DOMContentLoaded", function() {
    const countryInput = document.getElementById("countryInput");
    const countryDropdown = document.getElementById("countryDropdown");

    if (countryInput && countryDropdown) {
        console.log("Country input and dropdown found");

        countryInput.addEventListener("click", function() {
            console.log("Country input clicked");
            countryDropdown.style.display = "block";
        });

        document.addEventListener("click", function(event) {
            const isClickInside = countryInput.contains(event.target) || countryDropdown.contains(event.target);
            if (!isClickInside) {
                console.log("Click outside detected, hiding dropdown");
                countryDropdown.style.display = "none";
            }
        });
    } else {
        console.log("Country input or dropdown not found");
    }
});

function selectCountry(country) {
    const countryInput = document.getElementById("countryInput");
    const countryDropdown = document.getElementById("countryDropdown");

    if (countryInput && countryDropdown) {
        console.log(`Country selected: ${country}`);
        countryInput.value = country;
        countryDropdown.style.display = "none";
    }
}
