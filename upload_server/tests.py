"""Test objects used to test the endpoints of the upload server api.

Usage: manage.py test

Classes:
    UploadServerTestCase()
"""

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from upload_server.models import OrderItem, Upload


class UploadServerTestCase(APITestCase):
    """Contains the test cases for the upload server endpoints."""

    def test_create_upload_success(self):
        """Test successful creation of an upload."""
        upload = SimpleUploadedFile(
            "upload.txt",
            b"2 | Eggs | 20\n3 | Milk | 2",
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

    def test_read_upload_success(self):
        """Test successful retrieval of an upload."""
        upload = Upload()
        upload.insert()
        order_item = OrderItem(
            order_id=2,
            product_name="Eggs",
            product_quantity=20,
            upload=upload,
        )
        order_item.insert()
        response = self.client.get(
            reverse("read_upload", kwargs={"upload_id": upload.id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("number_of_rows"), 1)
        self.assertEqual(response.data.get("items"), ["Eggs"])

    def test_read_upload_does_not_exist_fail(self):
        """Test failed upload retrieval when upload does not exist."""
        response = self.client.get(
            reverse("read_upload", kwargs={"upload_id": 1})
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_read_upload_wrong_method_fail(self):
        """Test that only get method allowed at /upload/id endpoint."""
        response = self.client.delete(
            reverse("read_upload", kwargs={"upload_id": 1})
        )

        self.assertEqual(
            response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED
        )


class UploadServerIntegrationTestCase(APITestCase):
    """Contains the integration test cases for the upload server endpoints."""

    def test_can_upload_and_then_read_success(self):
        """Test successful upload and then retrieval of an upload."""
        upload = SimpleUploadedFile(
            "upload.txt",
            b"2 | Eggs | 20\n3 | Milk | 2",
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

        response = self.client.get(
            reverse("read_upload", kwargs={"upload_id": upload_id})
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get("number_of_rows"), 2)
        self.assertEqual(response.data.get("items"), ["Eggs", "Milk"])
