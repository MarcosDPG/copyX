function loadSettingsPartial(target) {
    fetch(`/settings/${target}`, { headers: { "X-Requested-With": "XMLHttpRequest" } })
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