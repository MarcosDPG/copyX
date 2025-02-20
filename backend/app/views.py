from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.views import retrieve_user
from publications.models import Tweet

def welcome(request):
    return render(request, "index.html")

@login_required
def home(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/home.html")  # Carga solo la parte dinámica
    return render(request, "base.html", {"content_template": "partials/home.html"})  # Carga la página completa

@login_required
def profile(request, user_id = None):
    user_data = {
        "name": "",
        "user_name":"",
        "posts_count": 0,
    }
    if user_id:
        user_data = retrieve_user(user_id)
        tweet_count = Tweet.objects.filter(user_id=user_id).count()
        user_data["posts_count"] = tweet_count
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/profile.html", user_data)
    return render(request, "base.html", {"content_template": "partials/profile.html", **user_data})

@login_required
def search_view(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/search.html")
    return render(request, "base.html", {"content_template": "partials/search.html"})

@login_required
def settings_view(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/settings.html")
    return render(request, "base.html", {"content_template": "partials/settings.html"})

@login_required
def settings_partial(request, option):
    user_data = {
        "name": "elnombredelusuarioaca",
        "username":"elusernameaca",
        "birth": [2,3,2004], # dia - mes - año
    }
    if option == "account_options":
        return render(request, "partials/account_options.html", {**user_data})
    elif option == "preferences_options":
        return render(request, "partials/preferences_options.html", {**user_data})
    return None