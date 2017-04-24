from django.forms import TextInput, Textarea
from django.contrib import admin
from django.db import models
from .models import Customer, Supply, Product, Inventory, Order, StateSelection, PendingPurchase, PurchaseItem


# Register your models here.

class ProfitAdmin(admin.ModelAdmin):
	list_display = ['order_number', 'purchase_number']
	list_filter = ['order_number', 'purchase_number']

admin.site.register(Customer)
admin.site.register(Supply)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Order)
# admin.site.register(Purchase)
# admin.site.register(ProductModel)
# admin.site.register(Profit, ProfitAdmin)
admin.site.register(StateSelection)
admin.site.register(PendingPurchase)
admin.site.register(PurchaseItem)
