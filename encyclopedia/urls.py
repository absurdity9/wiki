from django.urls import path

from . import views

urlpatterns = [
    path("search/", views.search, name="search"),
    path("", views.index, name="index"),
    path("new/", views.new, name="new"),
    path("wiki/<str:title>", views.wiki, name="wiki"),
    path("wiki/<str:title>/edit", views.edit, name="edit"),
    path("wiki/<str:title>/editor", views.editor, name="editor"),
    path("random/", views.randomentry, name="random"),
    path("<str:title>", views.directory, name="directory"),
]

