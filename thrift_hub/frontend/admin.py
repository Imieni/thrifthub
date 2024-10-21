from django.contrib import admin
from .models import Order
# Register your models here.

class  OrderAdmin(admin.ModelAdmin):
    list_display  = ["id", "ref", 'amount', "verified", "date_created"]

admin.site.register(Order)