from django.urls import path

from . import views

urlpatterns = [
    path("search/", views.search, name="search"),
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("random/", views.randomentry, name="random"),
    path("<str:title>", views.directory, name="directory"),
]

