function likeController(obj) {

    if (obj.classList.contains('liked') && obj.getAttribute('id-like')) {
        fetch(`/interactions/likes/${obj.getAttribute('id-like')}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
        })
        .then(response => {
            if (response.status === 200) {
                return response.json();
            }
            throw new Error("Error en la solicitud, código: " + response.status);
        })
        .then(data => {
            obj.removeAttribute('id-like');
            obj.classList.remove('liked');
            obj.nextElementSibling.textContent = parseInt(obj.nextElementSibling.textContent) - 1;
        });
    } else {
        fetch('/interactions/likes/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            credentials: 'include',
            body: JSON.stringify({object_id: obj.getAttribute('id-post'), type: obj.getAttribute('type-post')})
        })
        .then(response => {
            if (response.status === 201) {
                return response.json();
            }
            throw new Error("Error en la solicitud, código: " + response.status);
        })
        .then(data => {
            obj.setAttribute('id-like', data.like_id);
            obj.classList.add('liked');
            obj.nextElementSibling.textContent = parseInt(obj.nextElementSibling.textContent) + 1;
        });
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Busca el nombre del cookie al inicio de la cadena
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}