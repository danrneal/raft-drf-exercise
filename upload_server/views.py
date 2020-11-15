"""Views for the django upload server api.

Usage: manage.py runserver
"""

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, transaction
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from upload_server.models import OrderItem, Upload


def index(request):
    """Route Handler for the homepage.

    Args:
        request: A django request object
    """
    return "Hello world!"


class CreateUpload(APIView):
    """Route handler for the endpoint for creating a new upload.

    Attributes:
        parser_classes: An array of rest_framework parser objects that are used
            in this endpoint
    """

    parser_classes = [MultiPartParser]

    def post(self, request, format="txt"):
        """The handler for put requests on the endpoint to create new uploads.

        Args:
            request: A django request object
            format: A str representing the format of the data

        Returns:
            response: A json object representing info about the created upload
        """
        upload_file = request.data.get("file")
        if not upload_file:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        try:
            with transaction.atomic():
                upload = Upload()
                upload.insert()
                for line in upload_file.file:
                    order_data = line.decode("utf-8").split("|")
                    if len(order_data) != 3:
                        raise IntegrityError

                    order_item = OrderItem(
                        order_id=int(order_data[0]),
                        product_name=order_data[1].strip(),
                        product_quantity=int(order_data[2]),
                        upload=upload,
                    )
                    order_item.insert()
        except IntegrityError:
            return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        response = {"upload_id": upload.id}

        return Response(response, status=status.HTTP_201_CREATED)


@api_view(["GET"])
def read_upload(request, upload_id):
    """Route handler for the endpoint for retriving an upload.

    Args:
        request: A django request object
        upload_id: An int representing the id of the upload to retrieve

    Returns:
        response: A json object representing info about the retrieved upload
    """
    try:
        upload = Upload.objects.get(pk=upload_id)
    except ObjectDoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(upload.retrieve(), status=status.HTTP_200_OK)
