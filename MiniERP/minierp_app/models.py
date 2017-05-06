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


###############################################################

class Customer(models.Model):
	company_name = models.CharField(max_length=50)
	contact_name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=15)
	state = models.ForeignKey(StateSelection)
	zip_code = models.CharField(max_length=5)
	phone = models.CharField(max_length=15)
	fax = models.CharField(max_length=15,  null=True, blank=True)
	email = models.EmailField(max_length=60, null=True, blank=True)

	def __str__(self):
		return self.company_name

###############################################################

class Supply(models.Model):
	company_name = models.CharField(max_length=50)
	contact_name = models.CharField(max_length=30)
	address = models.CharField(max_length=50)
	city = models.CharField(max_length=15)
	state = models.ForeignKey(StateSelection)
	zip_code = models.CharField(max_length=5)
	phone = models.CharField(max_length=15)
	fax = models.CharField(max_length=15, null=True, blank=True)
	email = models.EmailField(max_length=60, null=True, blank=True)

	def __str__(self):
		return self.company_name


###############################################################

class Product(models.Model):
	supplier = models.ForeignKey(Supply)
	stock = models.IntegerField(default=0)
	name = models.CharField(max_length=25)
	model = models.CharField(max_length=20, default="", null=True, blank=True)
	dimention = models.CharField(max_length=20, default="", null=True, blank=True)
	weight = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
	price = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)
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


###############################################################

class PendingOrderItem(models.Model):
	user = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	product_amount = models.IntegerField(default=0)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)

	@property
	def total(self):
		return self.product_amount * self.product.price

	def __str__(self):
		return self.product.name

###############################################################

class CustomerOrder(models.Model):
	customer = models.ForeignKey(Customer)
	order_number = models.CharField(max_length=15)
	price = models.IntegerField(default=0)
	amount = models.IntegerField(default=0)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.order_number

###############################################################

class OrderItem(models.Model):
	order_number = models.CharField(max_length=15)
	product = models.ForeignKey(Product)
	product_amount = models.IntegerField(default=0)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)

	@property
	def total(self):
		return self.product_amount * self.product.price

	def __str__(self):
		return self.product.name



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


###############################################################

class PendingPurchaseItem(models.Model):
	user = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	product_amount = models.IntegerField(default=0)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)

	@property
	def total(self):
		return self.product_amount * self.product.price

	def __str__(self):
		return self.product.name


###############################################################

class PurchaseItem(models.Model):
	order_number = models.CharField(max_length=15)
	user = models.ForeignKey(User)
	product = models.ForeignKey(Product)
	product_amount = models.IntegerField(default=0)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)

	@property
	def total(self):
		return self.product_amount * self.product.price

	def __str__(self):
		return self.product.name

###############################################################

class PurchaseOrder(models.Model):
	order_number = models.CharField(max_length=15)
	# supplier = models.ForeignKey(Supply)
	price = models.IntegerField(default=0)
	amount = models.IntegerField(default=0)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.order_number

###############################################################

