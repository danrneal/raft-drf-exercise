from django.contrib import admin

from .models import OrderItem, Upload

admin.site.register(Upload)
admin.site.register(OrderItem)
