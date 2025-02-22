function loadResources(path="") {
    if (path.endsWith("/") && path.length > 1) {
        path = path.slice(0, -1);
    }
    user_id =  ""
    if (path.startsWith("/profile") && !path.endsWith("/profile")) {
        user_id = path.split("/")[2]
        path = "/profile/"
    }
    switch (path) {
        case "/":
            fetchTweets()
            break;
        case "/home":
            fetchTweets()
            break;
        case "/compose/post":
            history.back()
            break;
        case "/profile":
            switch (OptionSelected) {
                case 0:
                    fetchTweets(USER_ID)
                    break;
                case 1:
                    fetchRetweets(USER_ID)
                    break;
                case 2:
                    fetchLikes(USER_ID)
                    break;
                default:
                    break;
            }
            break;
        case "/profile/":
            switch (OptionSelected) {
                case 0:
                    fetchTweets(user_id)
                    break;
                case 1:
                    fetchRetweets(user_id)
                    break;
                case 2:
                    fetchLikes(user_id)
                    break;
                default:
                    break;
            }
            break;
        case "/settings":
            loadSettingsPartial()
            break;
        default:
            break;
    }
}

function fetchTweets(userid="") {
    fetch(`/tweets/${userid}`, { credentials: "include" })
    .then(response => response.text())
    .then(html => {
        const container = document.getElementById("post_container");
        container.innerHTML = html;
    })
    .catch(error => console.error("Error cargando datos:", error));
}

function fetchRetweets(userid="") {
    fetch(`/tweets/repost/${userid}`, { credentials: "include" })
    .then(response => response.text())
    .then(html => {
        const container = document.getElementById("post_container");
        container.innerHTML = html;
    })
    .catch(error => console.error("Error cargando datos:", error));
}

function fetchLikes(userid="") {
    fetch(`/tweets/like/${userid}`, { credentials: "include" })
    .then(response => response.text())
    .then(html => {
        const container = document.getElementById("post_container");
        container.innerHTML = html;
    })
    .catch(error => console.error("Error cargando datos:", error));
}

function loadSettingsPartial(target="") {
    if (target == "") {
        target = document.querySelector(".option_home_menu").getAttribute("data-target");
    }
    fetch(`/settings/${target}`, { headers: { "X-Requested-With": "XMLHttpRequest" }, credentials: "include" })
        .then(response => response.text())
        .then(html => {
            document.querySelector(".settings .column_menu").innerHTML = html;
        })
        .catch(err => console.error("Error cargando opciones:", err));
}

function toggleSelection(obj) {
    event.stopPropagation()
    let ignoredElements = ["INPUT", "BUTTON", "TEXTAREA", "SELECT"];
    if (ignoredElements.includes(event.target.tagName)) {
        return; 
    }
    obj.classList.toggle("selected");
}