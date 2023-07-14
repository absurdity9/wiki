from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.directory, name="directory"),
    path("new/", views.new, name="new"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("random/", views.randomentry, name="random"),
    path("layout/", views.search, name="search")
    #path("search/", views.search, name="search")
]

