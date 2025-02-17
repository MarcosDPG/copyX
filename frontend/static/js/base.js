document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            let url = this.getAttribute("href");

            if (url == "/") {
                url = "/home";
            }

            fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
                .then(response => response.text())
                .then(html => {
                    document.getElementById("content").innerHTML = html;
                    history.pushState(null, "", url);
                })
                .catch(err => console.error("Error cargando la vista:", err));
        });
    });

    window.addEventListener("popstate", function () {
        fetch(location.pathname, { headers: { "X-Requested-With": "XMLHttpRequest" } })
            .then(response => response.text())
            .then(html => {
                document.getElementById("content").innerHTML = html;
            });
    });
});