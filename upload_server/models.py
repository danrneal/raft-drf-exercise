"""Model objects used to model data for the db.

Classes:
    Upload()
    OrderItem()
"""

from django.db import models


class Upload(models.Model):
    """A model representing an upload."""

    def insert(self):
        """Inserts a new upload object into the db."""
        self.save()

    def retrieve(self):
        """Retrieves and formats the upload object as a dict.

        Returns:
            upload: A dict representing the upload object
        """
        items = [str(item) for item in self.order_items.all()]
        upload = {
            "upload_id": self.id,
            "number_of_rows": len(items),
            "items": items,
        }

        return upload

    def __str__(self):
        """An Upload object's str representation."""
        return f"Upload ID: {self.id}"


class OrderItem(models.Model):
    """A model representing an order item.

    Attributes:
        order_id: An int representing the id of the order the order item
            belongs to
        product_name: A str representing the name of the order item
        product_quantity: An int representing the quantity of the order item
        upload: An object representing the upload this order item belongs to
    """

    order_id = models.PositiveIntegerField()
    product_name = models.CharField(max_length=64)
    product_quantity = models.PositiveIntegerField()
    upload = models.ForeignKey(
        Upload, on_delete=models.CASCADE, related_name="order_items"
    )

    def insert(self):
        """Inserts a new order item object into the db."""
        self.save()

    def __str__(self):
        """An OrderItem object's str representation."""
        return f"{self.product_name}"
