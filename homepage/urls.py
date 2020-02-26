from django.urls import path
from homepage import views


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("privacy/", views.privacy, name="privacy")
]
