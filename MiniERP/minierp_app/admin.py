from django.forms import TextInput, Textarea
from django.contrib import admin
from django.db import models
from .models import Customer, Supply, Product, Inventory, PendingPurchaseItem, PurchaseItem, PurchaseOrder
from .models import Order, StateSelection, PendingOrderItem, CustomerOrder, OrderItem

# Register your models here.

class ProfitAdmin(admin.ModelAdmin):
	list_display = ['order_number', 'purchase_number']
	list_filter = ['order_number', 'purchase_number']

admin.site.register(Customer)
admin.site.register(Supply)
admin.site.register(Product)
admin.site.register(Inventory)
admin.site.register(Order)
admin.site.register(PurchaseOrder)
admin.site.register(PendingOrderItem)
admin.site.register(CustomerOrder)
admin.site.register(OrderItem)
# admin.site.register(ProductModel)
# admin.site.register(Profit, ProfitAdmin)
admin.site.register(StateSelection)
admin.site.register(PendingPurchaseItem)
admin.site.register(PurchaseItem)
