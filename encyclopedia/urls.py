from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:title>", views.directory, name="directory"),
    path("new/", views.new, name="new"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("random/", views.randomentry, name="random"),
    path("search/<str:title>", views.searchentry, name="search"),
]

