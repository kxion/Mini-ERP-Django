from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils import timezone
from decimal import Decimal


class StateSelection(models.Model):
	abbr = models.CharField(max_length=3)
	state = models.CharField(max_length=30)

	def __str__(self):
		return self.abbr + " - " + self.state

class Customer(models.Model):
	company_name = models.CharField(max_length=30)
	contact_name = models.CharField(max_length=30)
	address = models.CharField(max_length=25)
	city = models.CharField(max_length=15)
	state = models.ForeignKey(StateSelection)
	zip_code = models.CharField(max_length=5)
	phone = models.CharField(max_length=12)
	fax = models.CharField(max_length=12,  null=True, blank=True)
	note = models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return self.company_name

###############################################################
class Supply(models.Model):
	company_name = models.CharField(max_length=20)
	contact_name = models.CharField(max_length=20)
	address = models.CharField(max_length=25)
	city = models.CharField(max_length=15)
	state = models.ForeignKey(StateSelection)
	zip_code = models.CharField(max_length=5)
	phone = models.CharField(max_length=12)
	fax = models.CharField(max_length=12, null=True, blank=True)
	note = models.CharField(max_length=50, null=True, blank=True)

	def __str__(self):
		return self.company_name

###############################################################
class ProductModel(models.Model):
	product_name = models.CharField(max_length=25)
	product_model = models.CharField(max_length=25)

	def __str__(self):
		return self.product_model

###############################################################
class Product(models.Model):
	supplier = models.ForeignKey(Supply)
	stock = models.IntegerField(default=0)
	name = models.CharField(max_length=25)
	model = models.CharField(max_length=20, default="", null=True, blank=True)
	dimention = models.CharField(max_length=20, default="", null=True, blank=True)
	weight = models.DecimalField(max_digits=20, decimal_places=1, null=True, blank=True)
	price = models.IntegerField(default=0)
	photo = models.FileField(upload_to='products', blank=True)
	note = models.CharField(max_length=50, null=True, blank=True)
	create_time = models.DateTimeField(default=timezone.now)

	@property
	def photo_name(self):
		path = str(self.photo)
		start = path.index('/') + 1
		return path[start:]	

	def __str__(self):
		if self.stock <= 0:
			avaliable = " (out of stock)"
		else:
			avaliable = " (" + str(self.stock) + " in stock)"

		if self.model != "":
			return self.name + " --- " + self.model + avaliable
		else:
			return self.name + avaliable


##############################################################
class Inventory(models.Model):
	product = models.ForeignKey(Product)
	note = models.CharField(max_length=50, null=True, blank=True)
	buy = models.IntegerField(default=0)
	sell = models.IntegerField(default=0)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	@property
	def current(self):
		return self.buy - self.sell

	# def instock(self):
	# 	return self.product + "(" + self.current + " in stock)"

	def __str__(self):
		return self.product.name

##############################################################
class Order(models.Model):
	customer = models.ForeignKey(Customer)
	product = models.ForeignKey(Product)
	product_amount = models.IntegerField(default=0)
	sell_price = models.IntegerField(default=0)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	note = models.CharField(max_length=50, null=True, blank=True)
	@property
	def total(self):
		return self.product_amount * self.product.price

	# def __unicode__(self):
	# 	return self.pk
	def __str__(self):
		return self.customer.company_name

###############################################################
class Purchase(models.Model):
	product = models.ForeignKey(Product)
	product_amount = models.IntegerField(default=0)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	note = models.CharField(max_length=50, null=True, blank=True)

	@property
	def total(self):
		return self.product_amount * self.product.price

	def __str__(self):
		return self.product.name

###############################################################
class Profit(models.Model):
	order_number = models.ForeignKey(Order, blank=True, null=True)
	purchase_number = models.ForeignKey(Purchase, blank=True, null=True)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	note = models.CharField(max_length=50, null=True, blank=True)

	@property
	def amount(self):
		if not self.order_number:
			return self.purchase_number.product_amount 
		else:
			return self.order_number.product_amount 

	@property
	def unit_price(self):
		if not self.order_number:
			return self.purchase_number.purchase_price 
		else:
			return self.order_number.sell_price

	@property
	def total(self):
		if not self.order_number:
			return self.purchase_number.product_amount * self.purchase_number.purchase_price * -1
		else:
			return self.order_number.product_amount * self.order_number.sell_price

	def __int__(self):
		return self.pk
