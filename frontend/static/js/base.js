document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".nav-link").forEach(link => {
        link.addEventListener("click", function (e) {
            e.preventDefault();
            let url = this.getAttribute("href");
            if (url.endsWith("/") && url.length > 1) {
                url = url.slice(0, -1);
            }
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
        if (p.endsWith("/") && p.length > 1) {
            p = p.slice(0, -1);
        }
        if (p == "/compose/post") {
            composePost(false);
        } else {
            closeComposePost();
            if (p == "/") {
                p = "/home";
            }
            fetch(p, { headers: { "X-Requested-With": "XMLHttpRequest" } })
                .then(response => response.text())
                .then(html => {
                    document.getElementById("content").innerHTML = html;
                    changeIcon(location.pathname);
                });
        }
    });
    changeIcon(window.location.pathname);
});

function activeTextAreaPostCompose() {
    try {
        document.querySelectorAll(".post_compose_container .textarea_container textarea").forEach(area => {
            area.addEventListener("input", function () {
                this.style.height = "auto";
                this.style.height = (this.scrollHeight) + "px";
            });
        });

        document.querySelectorAll(".textarea_container").forEach(container => {
            container.addEventListener("submit", function (e) {
                e.preventDefault();
                let text = this.querySelector("textarea").value.trim();
            
                if (text) {
                    console.log("Publicando:", text);
                    // TODO realizar fecth y publicarlo
                }
            });
        });

    } catch (error) {}
}

function activeHomeMenuOptions() {
    document.querySelectorAll(".option_home_menu").forEach(option => {
        option.addEventListener("click", function () {
            let p = location.pathname;
            if (p.endsWith("/") && p.length > 1) {
                p = p.slice(0, -1);
            }
            switch (p) {
                case "/settings":
                    loadSettingsPartial(this.getAttribute("data-target"))
                    break;
                default:
                    break;
            }
            console.log(this.name)
            document.querySelectorAll(".option_home_menu").forEach(option =>{
                option.classList.remove("selected");
            })
            this.classList.add("selected");
        });
    });
}

function changeIcon(path) {
    activeTextAreaPostCompose();
    activeHomeMenuOptions();
    if (path.endsWith("/") && path.length > 1) {
        path = path.slice(0, -1);
    }
    if (path == "/compose/post") {
        history.pushState(null,"home","/");
        composePost(true);
    }
    if (path == "/home" || path == "/compose/post") {
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

function composePost(bool) {
    document.getElementById("cobertor").classList.add("active");
    if(bool) {
        history.pushState(null, '', '/compose/post');
        console.log("si");
    }
}

function closeComposePost() {
    document.getElementById("cobertor").querySelector("textarea").value = "";
    document.getElementById("cobertor").classList.remove("active");
}