from django.contrib import admin

from .models import Order, Upload

admin.site.register(Upload)
admin.site.register(Order)
