document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new FormData(form);
        const data = {
            name: formData.get("name"),
            birth_date: formData.get("birth_date"),
            user_name: formData.get("user_name"),
            email: formData.get("email"),
            password: formData.get("password"),
        };

        try {
            const response = await fetch("/users/auth/singup/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                window.location.href = "/users/auth/login";
            } else {
                const errorData = await response.json();
                alert(errorData.message || "Error en el registro. Inténtalo de nuevo.");
            }
        } catch (error) {
            console.error("Error al registrar:", error);
            alert("Ocurrió un error. Inténtalo más tarde.");
        }
    });
});
