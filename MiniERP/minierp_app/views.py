from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Customer, Supply, Product, Inventory, StateSelection, PendingPurchaseItem
from .models import PurchaseItem, PurchaseOrder, CustomerOrder, OrderItem, PendingOrderItem
from .forms import *
from twilio.rest import TwilioRestClient
from MiniERP.sms import send_sms
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
import string
import random

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
def customer_detail(request, id):
	error = ''
	success = ''
	customer = Customer.objects.get(id=id)
	orders = CustomerOrder.objects.filter(customer=customer)
	form = CustomerForm(initial={
								'company_name': customer.company_name,
                                'contact_name': customer.contact_name,
                                'address': customer.address,
                                'city': customer.city,
                                'state': customer.state,
                                'zip_code': customer.zip_code,
                                'fax': customer.fax,
                                'email': customer.email,
                                'phone': customer.phone })
	
	if request.method == 'POST':
		customer_form = CustomerForm(request.POST, request.FILES)
		if customer_form.is_valid():
			customer.company_name = customer_form.cleaned_data['company_name']
			customer.contact_name = customer_form.cleaned_data['contact_name']
			customer.address = customer_form.cleaned_data['address']
			customer.city = customer_form.cleaned_data['city']
			customer.state = customer_form.cleaned_data['state']
			customer.zip_code = customer_form.cleaned_data['zip_code']
			customer.fax = customer_form.cleaned_data['fax']
			customer.email = customer_form.cleaned_data['email']
			customer.phone = customer_form.cleaned_data['phone']
			customer.save()
			success = " The customer - " + customer.company_name + " - has been updated successfully!"

			customers = Customer.objects.all().order_by('company_name')
			form = CustomerForm()
			return render(request, 'customer/customer.html', {"customers": customers, "success": success, "form": form})
		else:
			error = "Data is not valid"
			return render(request, 'customer/customer_detail.html', {"customer": customer, "error": error, "form": form, "orders": orders})

	return render(request, 'customer/customer_detail.html', {"customer": customer,"form": form, "orders": orders})	


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
def supply_detail(request, id):
	error = ''
	success = ''
	supply = Supply.objects.get(id=id)
	products = Product.objects.filter(supplier=supply)
	form = SupplyForm(initial={
								'company_name': supply.company_name,
                                'contact_name': supply.contact_name,
                                'address': supply.address,
                                'city': supply.city,
                                'state': supply.state,
                                'zip_code': supply.zip_code,
                                'fax': supply.fax,
                                'email': supply.email,
                                'phone': supply.phone })
	
	if request.method == 'POST':
		supplier_form = SupplyForm(request.POST, request.FILES)
		if supplier_form.is_valid():
			supply.company_name = supplier_form.cleaned_data['company_name']
			supply.contact_name = supplier_form.cleaned_data['contact_name']
			supply.address = supplier_form.cleaned_data['address']
			supply.city = supplier_form.cleaned_data['city']
			supply.state = supplier_form.cleaned_data['state']
			supply.zip_code = supplier_form.cleaned_data['zip_code']
			supply.fax = supplier_form.cleaned_data['fax']
			supply.email = supplier_form.cleaned_data['email']
			supply.phone = supplier_form.cleaned_data['phone']
			supply.save()
			success = " The customer - " + supply.company_name + " - has been updated successfully!"

			supplies = Supply.objects.all().order_by('company_name')
			form = SupplyForm()
			return render(request, 'supply/supply.html', {"supplies": supplies, "success": success, "form": form})
		else:
			error = "Data is not valid"
			return render(request, 'supply/supply_detail.html', {"supply": supply, "error": error, "form": form, "products": products})

	return render(request, 'supply/supply_detail.html', {"supply": supply, "form": form, "products": products})	



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
	customerOrders = CustomerOrder.objects.all().order_by('create_time')
	return render(request, 'customer/customer_order.html', {'customerOrders': customerOrders})

###############################################################	
@login_required(login_url="/")
def purchase_management(request):
	purchaseOrders = PurchaseOrder.objects.all().order_by('create_time')
	return render(request, 'supply/purchase_order.html', {'purchaseOrders': purchaseOrders})


###############################################################
@login_required(login_url="/")
def purchase_order_details(request, id):
	items = PurchaseItem.objects.filter(order_number=id)
	order = PurchaseOrder.objects.get(order_number=id)
	total_price = 0
	for item in items:
		total_price += (item.product.price * item.product_amount)
	print("total price = " + str(total_price))
	return render(request, 'supply/purchase_order_details.html', {'items': items, 'total_price': total_price, 'order':order})

###############################################################
@login_required(login_url="/")
def customer_order_details(request, id):
	items = OrderItem.objects.filter(order_number=id)
	order = CustomerOrder.objects.get(order_number=id)
	total_price = 0
	for item in items:
		total_price += (item.product.price * item.product_amount)
	return render(request, 'customer/customer_order_details.html', {'items': items, 'total_price': total_price, 'order':order})

###############################################################

@login_required(login_url="/")
def add_purchase(request, id):
	print()
	error = ''
	success = ''
	product = Product.objects.get(id=id)
	form = AmountForm(initial={'product_amount':1,})
	
	if request.method == 'POST':
		amount_form = AmountForm(request.POST, request.FILES)
		if amount_form.is_valid():
			qty = amount_form.cleaned_data['amount']
			pending_items = PendingPurchaseItem.objects.filter(product=product,user=request.user)
			
			if len(pending_items) == 0:
				pending_item = PendingPurchaseItem(product=product,user=request.user,product_amount=qty)
				pending_item.save()
				print("ok save")
			else:
				pending_item = PendingPurchaseItem.objects.get(product=product,user=request.user)
				pending_item.product_amount = qty
				pending_item.save()
				print("ok save 2")
			
			success = " The product '" + product.name + "' has been add to pending purchse with QTY " + str(qty)
			url = '/create_purchase/?message=' + success
			products = Product.objects.all().order_by('supplier')
			pending_items = PendingPurchaseItem.objects.filter(user=request.user)
			return redirect(url)
		else:
			error = "Data is not valid"
			return render(request, 'supply/add_pending_item.html', {"product": product, "error": error, "form": form})
	
	return render(request, 'supply/add_pending_item.html', {"product": product, "form": form})


###############################################################

@login_required(login_url="/")
def add_order_item(request, id):
	print()
	error = ''
	success = ''
	product = Product.objects.get(id=id)
	form = AmountForm(initial={'product_amount':1,})
	
	if request.method == 'POST':
		amount_form = AmountForm(request.POST, request.FILES)
		if amount_form.is_valid():
			qty = amount_form.cleaned_data['amount']
			inventory_item = Inventory.objects.get(product=product)
			if inventory_item.current < qty:
				error = 'Insufficient stock: This product currently have ' + str(inventory_item.current) + ' in stock'
				return render(request, 'supply/add_pending_item.html', {"product": product, "error": error, "form": form})


			pending_items = PendingOrderItem.objects.filter(product=product,user=request.user)
			
			if len(pending_items) == 0:
				pending_item = PendingOrderItem(product=product,user=request.user,product_amount=qty)
				pending_item.save()
				print("ok save")
			else:
				pending_item = PendingOrderItem.objects.get(product=product,user=request.user)
				pending_item.product_amount = qty
				pending_item.save()
				print("ok save 2")
			
			success = " The product '" + product.name + "' has been add to pending order with QTY " + str(qty)
			url = '/create_order/?message=' + success
			return redirect(url)

		else:
			error = "Data is not valid"
			return render(request, 'supply/add_pending_item.html', {"product": product, "error": error, "form": form})
	
	return render(request, 'supply/add_pending_item.html', {"product": product, "form": form})


###############################################################	
@login_required(login_url="/")
def create_purchase(request):
	if request.GET.get('message') != None:
		print("get value: " + request.GET.get('message'))
	error = ''
	success = request.GET.get('message', '')
	print("message = " + success)

	# form = ProductForm()
	products = Product.objects.all().order_by('supplier')
	pending_items = PendingPurchaseItem.objects.filter(user=request.user)
	if request.method == 'POST' and len(pending_items) != 0:
		order_number = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
		purchase_items = PurchaseItem.objects.filter(order_number=order_number)

		while len(purchase_items) != 0:
			print(order_number + ' already exist!')
			order_number = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
			purchase_items = PurchaseItem.objects.filter(order_number=order_number)

		total_price = 0
		total_amount = 0

		for item in pending_items:
			total_price = total_price + item.total
			total_amount = total_amount + item.product_amount
			purchase_item = PurchaseItem.objects.create(order_number=order_number,
														user=request.user,
														product= item.product,
														product_amount=item.product_amount)
			purchase_item.save()
			item.delete()
			inventory_item = Inventory.objects.get(product=purchase_item.product)
			inventory_item.buy = inventory_item.buy + purchase_item.product_amount
			inventory_item.save()
			
			product_item = Product.objects.get(pk=purchase_item.product.pk)
			product_item.stock = product_item.stock + purchase_item.product_amount
			product_item.save()
		
		purchase_orders = PurchaseOrder.objects.create(order_number=order_number,
													   price=total_price,
													   amount=total_amount)
		purchase_orders.save()
		
		success = 'The Purchase has been created successfully with order# ' + order_number + '.'
		return render(request, 'supply/create_purchase.html', {"products": products, "success": success})

	return render(request, 'supply/create_purchase.html', {"products": products, "pending_items": pending_items, "success": success})


###############################################################	
@login_required(login_url="/")
def create_order(request):
	form = CustomerSelectForm()
	# if request.GET.get('message') != None:
	# 	print("get value: " + request.GET.get('message'))
	error = ''
	success = request.GET.get('message', '')
	print("message = " + success)

	products = Product.objects.all().order_by('supplier')
	pending_items = PendingOrderItem.objects.filter(user=request.user)

	if request.method == 'POST' and len(pending_items) != 0:
		customer_form = CustomerSelectForm(request.POST, request.FILES)
		if customer_form.is_valid():
			customer = customer_form.cleaned_data['customer']

		order_number = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
		purchase_items = OrderItem.objects.filter(order_number=order_number)

		while len(purchase_items) != 0:
			print(order_number + ' already exist!')
			order_number = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(15))
			purchase_items = PurchaseItem.objects.filter(order_number=order_number)

		total_price = 0
		total_amount = 0
		for item in pending_items:
			total_price = total_price + item.total
			total_amount = total_amount + item.product_amount
			order_item = OrderItem.objects.create(order_number=order_number,
														product= item.product,
														product_amount=item.product_amount)
			order_item.save()
			item.delete()

			inventory_item = Inventory.objects.get(product=item.product)
			inventory_item.sell = inventory_item.sell + item.product_amount
			inventory_item.save()
			
			product_item = Product.objects.get(pk=item.product.pk)
			product_item.stock = product_item.stock - item.product_amount
			product_item.save()
		
		customer_order = CustomerOrder.objects.create(order_number=order_number,
														customer=customer,	
														price=total_price,
														amount=total_amount)
		customer_order.save()	
		success = 'The Purchase has been created successfully with order# ' + order_number + '.'
		return render(request, 'customer/create_order.html', {"products": products, "success": success, "form": form})

	return render(request, 'customer/create_order.html', 
		{"products": products, "pending_items": pending_items, "success": success, "form": form})

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


################################################################

@login_required(login_url="/")
def delete_purchase_item(request, id):
	print(id)
	pending_item = PendingPurchaseItem.objects.get(id=id)
	pending_item.delete()	
	url = '/create_purchase/'
	return redirect(url)


################################################################

@login_required(login_url="/")
def delete_order_item(request, id):
	print(id)
	pending_item = PendingOrderItem.objects.get(id=id)
	pending_item.delete()	
	url = '/create_order/'
	return redirect(url)

###############################################################
@login_required(login_url="/")
def profit_and_revenue(request):
	profits = Profit.objects.all().order_by('id')
	return render(request, 'sales/profit_and_revenue.html', {"profits": profits})
