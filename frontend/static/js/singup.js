document.addEventListener("DOMContentLoaded", function () {
    const form = document.querySelector("form");

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const formData = new URLSearchParams(new FormData(form));

        try {
            const response = await fetch("/users/auth/singup/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                    "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
                },
                body: formData.toString(),
            });

            if (response.ok) {
                window.location.href = "/users/auth/login/";
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
