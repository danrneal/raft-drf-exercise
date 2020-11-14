"""Model objects used to model data for the db.

Classes:
    Upload()
    Order()
"""

from django.db import models


class Upload(models.Model):
    """A model representing an upload."""

    def retrieve(self):
        """Retrieves and formats the upload object as a dict.

        Returns:
            upload: A dict representing the upload object
        """
        upload = {
            "upload_id": self.id,
            "number_of_rows": len(self.orders),
            "items": [order.product_name for order in self.orders],
        }

        return upload


class Order(models.Model):
    """A model representing an order.

    Attributes:
        product_name: A str representing the name of the product ordered
        product_quantity: An int representing the quantity of the product
            ordered
        upload: An object representing the upload this order belongs to
    """

    product_name = models.CharField(max_length=64)
    product_quantity = models.PositiveIntegerField()
    upload = models.ForeignKey(
        Upload, on_delete=models.CASCADE, related_name="orders"
    )

    def insert(self):
        """Inserts a new order object into the db."""
        self.save()

    def __str__(self):
        """An Order object's str representation."""
        return f"{self.product_name}"
