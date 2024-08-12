document.getElementById("countryInput").addEventListener("click", function() {
    document.getElementById("countryDropdown").style.display = "block";
});

function selectCountry(country) {
    document.getElementById("countryInput").value = country;
    document.getElementById("countryDropdown").style.display = "none";
}

document.addEventListener("click", function(event) {
    var isClickInside = document.getElementById("countryInput").contains(event.target);
    if (!isClickInside) {
        document.getElementById("countryDropdown").style.display = "none";
    }
});