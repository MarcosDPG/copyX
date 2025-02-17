document.addEventListener("DOMContentLoaded", function () {

    const textarea = document.querySelector(".post_compose_container .textarea_container textarea");

    textarea.addEventListener("input", function () {
        this.style.height = "auto";
        this.style.height = (this.scrollHeight) + "px";
    });

    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            let url = this.getAttribute("href");

            if (url == "/") {
                url = "/home";
            }

            if (isSamePath(location.pathname,url)) {
                fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } })
                    .then(response => response.text())
                    .then(html => {
                        document.getElementById("content").innerHTML = html;
                        if (url == "/home") {
                            url = "/";
                        }
                        history.pushState(null, "", url);
                        changeIcon(url);
                    })
                    .catch(err => console.error("Error cargando la vista:", err));
            }
        });
    });

    window.addEventListener("popstate", function () {
        let p = location.pathname;
        if (p == "/") {
            p = "/home";
        }
        fetch(p, { headers: { "X-Requested-With": "XMLHttpRequest" } })
            .then(response => response.text())
            .then(html => {
                document.getElementById("content").innerHTML = html;
                changeIcon(location.pathname);
            });
    });

    changeIcon(window.location.pathname);
});

function changeIcon(path) {
    if (path.endsWith("/") && path.length > 1) {
        path = path.slice(0, -1);
    }
    if (path == "/home" || path == "/home/") {
        path = "/";
    }
    document.querySelectorAll(".icon_menu").forEach(icon => icon.setAttribute("fill", "none"));

    let activeLink = document.querySelector(`.nav-link[href="${path}"]`);
    if (activeLink) {
        activeLink.querySelector(".icon_menu").setAttribute("fill", "white");
    }
}

function isSamePath(url1, url2) {
    if (url1.endsWith("/") && url1.length > 1) {
        url1 = url1.slice(0, -1);
    }
    if (url1 == "/home") {
        url1="/"
    }
    if (url2.endsWith("/") && url2.length > 1) {
        url2 = url2.slice(0, -1);
    }
    if (url2 == "/home") {
        url2="/"
    }
    return url1 !== url2;
}