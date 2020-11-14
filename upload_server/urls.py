from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/upload", views.create_upload, name="create_upload"),
    path("api/<int:upload_id>", views.read_upload, name="read_upload"),
]
