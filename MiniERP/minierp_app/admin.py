from django.forms import TextInput, Textarea
from django.contrib import admin
from django.db import models
from .models import Customer, Supply, Product, Stock, Order, Purchase, Profit

# Register your models here.

class ProfitAdmin(admin.ModelAdmin):
	list_display = ['order_number', 'purchase_number']
	list_filter = ['order_number', 'purchase_number']

admin.site.register(Customer)
admin.site.register(Supply)
admin.site.register(Product)
admin.site.register(Stock)
admin.site.register(Order)
admin.site.register(Purchase)
admin.site.register(Profit, ProfitAdmin)