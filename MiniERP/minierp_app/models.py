from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils import timezone

class Customer(models.Model):
	company_name = models.CharField(max_length=20)
	contact_name = models.CharField(max_length=20)
	address = models.CharField(max_length=25)
	city = models.CharField(max_length=15)
	state = models.CharField(max_length=2)
	zip_code = models.CharField(max_length=5)
	phone = models.CharField(max_length=12)
	fax = models.CharField(max_length=12)

	def __str__(self):
		return self.company_name

###############################################################
class Supply(models.Model):
	company_name = models.CharField(max_length=20)
	contact_name = models.CharField(max_length=20)
	address = models.CharField(max_length=25)
	city = models.CharField(max_length=15)
	state = models.CharField(max_length=2)
	zip_code = models.CharField(max_length=5)
	phone = models.CharField(max_length=12)
	fax = models.CharField(max_length=12)

	def __str__(self):
		return self.company_name

###############################################################
class Product(models.Model):
	supplier = models.ForeignKey(Supply)
	product_name = models.CharField(max_length=25)
	product_model = models.CharField(max_length=20)
	unit = models.CharField(max_length=5)
	note = models.CharField(max_length=50)

	def __str__(self):
		return self.product_name

###############################################################
class Stock(models.Model):
	product = models.ForeignKey(Product)
	note = models.CharField(max_length=50)
	purchase = models.IntegerField(default=0)
	sell = models.IntegerField(default=0)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	@property
	def current(self):
		return self.purchase - self.sell

	def __str__(self):
		return self.product.product_name

###############################################################
class Order(models.Model):
	customer = models.ForeignKey(Customer)
	product = models.ForeignKey(Product)
	product_amount = models.IntegerField(default=0)
	sell_price = models.IntegerField(default=0)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	note = models.CharField(max_length=50)
	@property
	def total(self):
		return self.product_amount * self.sell_price

	# def __unicode__(self):
	# 	return self.pk
	def __str__(self):
		return self.customer.company_name

###############################################################
class Purchase(models.Model):
	product = models.ForeignKey(Product)
	product_amount = models.IntegerField(default=0)
	purchase_price = models.IntegerField(default=0)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	note = models.CharField(max_length=50)
	@property
	def total(self):
		return self.product_amount * self.purchase_price

	def __str__(self):
		return self.product.product_name

###############################################################
class Profit(models.Model):
	order_number = models.ForeignKey(Order, blank=True, null=True)
	purchase_number = models.ForeignKey(Purchase, blank=True, null=True)
	create_time = models.DateTimeField(default=timezone.now)
	updated = models.DateTimeField(auto_now=True)
	note = models.CharField(max_length=50)

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
