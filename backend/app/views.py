from django.shortcuts import render

def base(request):
    return render(request, "base.html", {"content_template": "partials/home.html"})

def home(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/home.html")  # Carga solo la parte dinámica
    return render(request, "base.html", {"content_template": "partials/home.html"})  # Carga la página completa

def profile(request):
    user_data = {
        "name": "elnombredelusuarioaca",
        "username":"elusernameaca",
        "posts_count": 0,
    }
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/profile.html", {**user_data})
    return render(request, "base.html", {"content_template": "partials/profile.html", **user_data})

def settings_view(request):  
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/settings.html")
    return render(request, "base.html", {"content_template": "partials/settings.html"})
