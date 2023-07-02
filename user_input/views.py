from django.shortcuts import render
from .forms import UserResponseForm
from .openai_requests import generate_storyline
import json


def home(request):
    storyline = []
    if request.method == "POST":
        form = UserResponseForm(request.POST)
        if form.is_valid():
            age = form.cleaned_data["age"]
            interests = form.cleaned_data["interests"]
            topic = form.cleaned_data["topic"]
            storyline = generate_storyline(age, interests, topic)
            print(storyline)
            storyline_json = json.dumps(storyline)
            return render(
                request, "home.html", {"form": form, "storyline": storyline_json}
            )

    else:
        form = UserResponseForm()
    return render(request, "home.html", {"form": form})
