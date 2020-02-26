from django.shortcuts import render


def homepage(request):
    return render(request, "homepage.html", {})


def privacy(request):
    return render(request, "privacy.html", {})
