"""Test objects used to test the endpoints of the upload server api.

Usage: manage.py test

Classes:
    UploadServerTestCase()
"""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from upload_server.models import Upload


class UploadServerTestCase(APITestCase):
    """Contains the test cases for the upload server endpoints."""

    def test_create_upload_success(self):
        """Test successful creation of an upload."""
        upload = SimpleUploadedFile(
            "upload.txt",
            b"2 | Eggs | 20",
            content_type="text/plain",
        )
        response = self.client.post(
            reverse("create_upload"),
            {"file": upload},
        )
        upload_id = response.data.get("upload_id")
        upload = Upload.objects.get(pk=upload_id)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIsNotNone(upload)

    def test_create_upload_malformed_data_fail(self):
        """Test failed upload creation when data is malformed."""
        upload = SimpleUploadedFile(
            "upload.txt", b"eggs", content_type="text/plain"
        )
        response = self.client.post(reverse("create_upload"), {"file": upload})

        self.assertEqual(
            response.status_code, status.HTTP_422_UNPROCESSABLE_ENTITY
        )

    def test_create_upload_missing_data_fail(self):
        """Test failed upload creation when data is missing."""
        response = self.client.post(reverse("create_upload"), {"file": ""})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_upload_wrong_method_fail(self):
        """Test that only post method allowed at /upload endpoint."""
        response = self.client.get(reverse("create_upload"))

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )
