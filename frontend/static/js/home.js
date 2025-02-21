document.addEventListener("DOMContentLoaded", function () {
    fetch("/tweets/", { credentials: "include" })
        .then(response => response.text())
        .then(html => {
            const container = document.getElementById("post_container");
            container.innerHTML = html;
        })
        .catch(error => console.error("Error cargando datos:", error));
});