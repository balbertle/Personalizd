window.addEventListener("beforeunload", function () {
    const selectedRating = document.querySelector('input[name="rating"]:checked');
    if (selectedRating) {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", window.location.href, true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.send("rating=" + selectedRating.value);
    }
});