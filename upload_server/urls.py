from django.urls import path

from . import views

urlpatterns = [
    path("api/upload", views.CreateUpload.as_view(), name="create_upload"),
    path("api/upload/<int:upload_id>", views.read_upload, name="read_upload"),
]
