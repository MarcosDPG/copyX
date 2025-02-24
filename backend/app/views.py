from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from users.views import retrieve_user
from publications.models import Tweet
from django.shortcuts import redirect

def welcome(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, "index.html")

@login_required
def home(request):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/home.html")  # Carga solo la parte dinámica
    return render(request, "base.html", {"content_template": "partials/home.html"})  # Carga la página completa

@login_required
def profile(request, user_id = None):
    # Search for the user_id in case it is not the authenticated user
    user_id = user_id or request.user.user_id
    # Count the number of tweets associated with the user
    tweet_count = Tweet.objects.filter(user_id=user_id).count()
    # Retrieve the user data in form of a dictionary
    user_data = retrieve_user(user_id)
    # Add the number of tweets to the user data
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
        "name": request.user.name,
        "user_name":request.user.user_name,
        "birth": str(request.user.birth_date).split("-"), # año - mes - dia
    }
    if option == "account_options":
        return render(request, "partials/account_options.html", {**user_data})
    elif option == "preferences_options":
        return render(request, "partials/preferences_options.html", {**user_data})
    return None

@login_required
def post_view(request, post_id):
    if request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return render(request, "partials/post_view.html")
    return render(request, "base.html", {"content_template": "partials/post_view.html"})