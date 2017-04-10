from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Customer, Supply, Product, Inventory, Order, Purchase, Profit, ProductModel, StateSelection
from .forms import *
from twilio.rest import TwilioRestClient
from MiniERP.sms import send_sms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User


# for registration
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from registration.backends.default.views import RegistrationView
from registration.forms import RegistrationFormUniqueEmail

# for email
from django.core.mail import send_mail


###############################################################
def home(request):
	return render(request, 'home.html')

###############################################################
@login_required(login_url="/")
def user_management(request, is_super):
	if is_super == "super_user":
		users = User.objects.filter(is_active=True, is_superuser=True).order_by('-is_superuser')
		# users = User.objects.all().order_by('-is_superuser')
		return render(request, 'user/user.html', {"users": users})
	else:
		users = User.objects.filter(is_active=True, is_superuser=False).order_by('-is_superuser')
		# users = User.objects.all().order_by('-is_superuser')
		return render(request, 'user/user.html', {"users": users})

###############################################################
@login_required(login_url="/")
def customer_management(request):
	error = ''
	success = ''
	form = CustomerForm()
	customers = Customer.objects.all().order_by('company_name')

	if request.method == 'POST':
		customer_form = CustomerForm(request.POST, request.FILES)
		if customer_form.is_valid():
			customer = customer_form.save(commit=False)
			customer.save()
			success = "Adding new customer completed"
			customers = Customer.objects.all().order_by('company_name')
			return render(request, 'customer/customer.html', {"customers": customers, "success": success, "form": form})
		else:
			error = "Data is not valid"
			return render(request, 'customer/customer.html', {"customers": customers, "error": error, "form": form})

	return render(request, 'customer/customer.html', {"customers": customers, "form": form})	

###############################################################
@login_required(login_url="/")
def supply_management(request):
	error = ''
	success = ''
	form = SupplyForm()
	supplies = Supply.objects.all().order_by('company_name')

	if request.method == 'POST':
		supplier_form = SupplyForm(request.POST, request.FILES)
		if supplier_form.is_valid():
			supplier = supplier_form.save(commit=False)
			supplier.save()
			success = "Adding new supplier completed"
			supplies = Supply.objects.all().order_by('company_name')
			return render(request, 'supply/supply.html', {"supplies": supplies, "success": success, "form": form})
		else:
			error = "Data is not valid"
			return render(request, 'supply/supply.html', {"supplies": supplies, "error": error, "form": form})

	return render(request, 'supply/supply.html', {"supplies": supplies, "form": form})






###############################################################
@login_required(login_url="/")
def product_detail(request, id):
	print()
	error = ''
	success = ''
	product = Product.objects.get(id=id)
	form = ProductForm(initial={
								'name': product.name,
                                'supplier': product.supplier,
                                'model': product.model,
                                'dimention': product.dimention,
                                'weight': product.weight,
                                'price': product.price,
                                'note': product.note })
	
	if request.method == 'POST':
		product_form = ProductForm(request.POST, request.FILES)
		if product_form.is_valid():
			print(product_form.cleaned_data['photo'])
			if product_form.cleaned_data['photo'] != None:
				product.photo = product_form.cleaned_data['photo']
			product.supplier = product_form.cleaned_data['supplier']
			product.model = product_form.cleaned_data['model']
			product.dimention = product_form.cleaned_data['dimention']
			product.weight = product_form.cleaned_data['weight']
			product.price = product_form.cleaned_data['price']
			product.note = product_form.cleaned_data['note']
			product.name = product_form.cleaned_data['name']
			product.save()
			
			success = " The product - " + product.name + " - has been updated successfully!"
			products = Product.objects.all().order_by('id')
			form = ProductForm()
			return render(request, 'product/product.html', {"products": products, "success": success, "form": form})
		else:
			error = "Data is not valid"
			return render(request, 'product/product_detail.html', {"product": product, "error": error, "form": form})
	
	return render(request, 'product/product_detail.html', {"product": product, "form": form})






###############################################################
@login_required(login_url="/")
def product_management(request):
	error = ''
	success = ''
	form = ProductForm()
	products = Product.objects.all().order_by('id')

	if request.method == 'POST':
		product_form = ProductForm(request.POST, request.FILES)
		if product_form.is_valid():
			name = product_form.cleaned_data['name']
			model = product_form.cleaned_data['model']
			product = product_form.save(commit=False)
			product.save()
			inventory = Inventory(product=Product.objects.get(name=name, model=model))
			inventory.save()

			if not ProductModel.objects.filter(product_name=name):
				product_model = ProductModel(product_name=name, product_model=model)
				product_model.save()
			success = "Adding new product completed"
			products = Product.objects.all().order_by('id')
			return render(request, 'product/product.html', {"products": products, "success": success, "form": form})
		else:
			error = "Data is not valid"
			return render(request, 'product/product.html', {"products": products, "error": error, "form": form})
	
	return render(request, 'product/product.html', {"products": products, "form": form})

###############################################################
@login_required(login_url="/")
def order_management(request):
	request.session['name'] = "hello"
	error = ''
	success = ''
	orders = Order.objects.all().order_by('id')
	form = OrderForm()
	if request.method == 'POST':
		order_form = OrderForm(request.POST, request.FILES)
		if order_form.is_valid():
			product = order_form.cleaned_data['product']
			print(product.name)
			amount = order_form.cleaned_data['product_amount']
			print(amount)

			inventory = Inventory.objects.get(product=product)

			if inventory.current < amount:
				error = 'Understock: Current stock is ' + str(product.stock) + ", please adjust the amount or contact the company."
				# ", please reduce the amount or come back later!'
				return render(request, 'customer/order.html', {"orders": orders, "error": error, "form": form})
			else:	
				inventory.sell = inventory.sell + amount
				inventory.save()

				product.stock = product.stock - amount
				product.save()

				order = order_form.save(commit=False)
				order.save()
				success = "Adding new order completed"
				orders = Order.objects.all().order_by('id')
				return render(request, 'customer/order.html', {"orders": orders, "success": success, "form": form})
		else:
			print("fail!!!")
			error = "Data is not valid"
			return render(request, 'customer/order.html', {"orders": orders, "error": error, "form": form})
	
	return render(request, 'customer/order.html', {"orders": orders, "form": form})

###############################################################	
@login_required(login_url="/")
def purchase_management(request):
	form = PurchaseForm()
	success = ''
	purchases = Purchase.objects.all().order_by('id')

	if request.method == 'POST':
		purchase_form = PurchaseForm(request.POST, request.FILES)
		if purchase_form.is_valid():
			product = purchase_form.cleaned_data['product']
			amount = purchase_form.cleaned_data['product_amount']
			purchase = purchase_form.save(commit=False)
			purchase.save()
			inventory = Inventory.objects.get(product=product)
			inventory.buy = inventory.buy + amount
			inventory.save()
			product.stock = product.stock + amount
			product.save()
			print(inventory.buy)
			success = "Adding new purchase completed"
			purchases = Purchase.objects.all().order_by('id')
			return render(request, 'supply/purchase.html', {"purchases": purchases, "success": success, "form": form})
		else:
			print("fail!!!")
			error = "Data is not valid"
			return render(request, 'supply/purchase.html', {"purchases": purchases, "error": error, "form": form})
	
	return render(request, 'supply/purchase.html', {"purchases": purchases, "form": form})


###############################################################	
@login_required(login_url="/")
def create_purchase(request):
	error = ''
	success = ''
	form = ProductForm()
	products = Product.objects.all().order_by('supplier')

	if request.GET.get('id') != None:
		product_id = int(request.GET.get('id'))
		product = Product.objects.get(id=product_id)
		print("ok")
		return render(request, 'supply/create_purchase.html', {"products": products, "product": product})
	# products = Product.objects.all().order_by('id')
	return render(request, 'supply/create_purchase.html', {"products": products})


###############################################################
@login_required(login_url="/")
def inventory_management(request):
	inventories = Inventory.objects.all().order_by('product')
	if request.GET.get('id') != None:
		product_id = int(request.GET.get('id'))
		product = Product.objects.get(id=product_id)
		print("ok")
		return render(request, 'product/inventory.html', {"inventories": inventories, "product": product})
	# products = Product.objects.all().order_by('id')
	return render(request, 'product/inventory.html', {"inventories": inventories})



# ###############################################################
# @login_required(login_url="/")
# def inventory_management(request, id):
# 	inventories = Inventory.objects.all().order_by('product')
# 	product = Product.objects.get(id=id)
# 	# products = Product.objects.all().order_by('id')
# 	return render(request, 'product/inventory.html', {"inventories": inventories, "product": product})







###############################################################
@login_required(login_url="/")
def profit_and_revenue(request):
	profits = Profit.objects.all().order_by('id')
	return render(request, 'sales/profit_and_revenue.html', {"profits": profits})
