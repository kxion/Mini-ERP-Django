from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Customer, Supply, Product, Stock, Order, Purchase, Profit
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


# Create your views here.

class RegistrationViewUniqueEmail(RegistrationView):
    form_class = RegistrationFormUniqueEmail


def send_email(subject, user):
	
	message = "Dear %s, \nThanks for your registration ~ Now you can start to make your business! Enjoy !" % (user.username,)
	from_email = settings.DEFAULT_FROM_EMAIL
	to_email = [settings.EMAIL_HOST_USER, user.email]

	send_mail(subject, 
				message, 
				from_email, 
				to_email, 
				fail_silently=False)

###############################################################
@csrf_protect
def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = User.objects.create_user(
			username=form.cleaned_data['username'],
			password=form.cleaned_data['password1'],
			email=form.cleaned_data['email']
			)
			profile = Profile(user_id=user.id)
			profile.email = user.email
			profile.save()

			### email test
			subject = 'Welcome to MiniERP!'
			# message = 'just test'
			# from_email = settings.EMAIL_HOST_USER
			# to_email = [settings.EMAIL_HOST_USER]

			send_email(subject, user)
			
			# send_mail(subject, 
			# 		message, 
			# 		from_email, 
			# 		to_email, 
			# 		fail_silently=False)
			### end of email test

			return HttpResponseRedirect('/register/success/')
		# else:
		# 	return redirect('/')
	else:
		form = RegistrationForm()

	variables = RequestContext(request, {'form': form})

	return render_to_response('registration/register.html', variables,)
	# return render_to_response('registration/register.html', {'form': form},)
 
###############################################################
def register_success(request):
    return render_to_response(
    'registration/success.html',
    )

###############################################################
# Create user profile after receiving activation signal
# from registration.signals import user_registered
# def user_registered_profile(sender, user, request, **kwargs):
# 	profile = Profile(user_id=user.id)
# 	profile.email = user.email
# 	profile.save()
# 	user_registered.connect(user_registered_profile)

###############################################################
def home(request):
	return render(request, 'home.html')

###############################################################
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
def customer_management(request):
	users = User.objects.filter(is_active=True).order_by('-is_superuser')
	# users = User.objects.all().order_by('-is_superuser')
	customers = Customer.objects.all().order_by('company_name')
	return render(request, 'customer/customer.html', {"customers": customers})	

###############################################################
def supply_management(request):
	supplies = Supply.objects.all().order_by('company_name')
	return render(request, 'supply/supply.html', {"supplies": supplies})

###############################################################
def product_management(request):
	products = Product.objects.all().order_by('supplier')
	return render(request, 'product/product.html', {"products": products})

###############################################################
def stock_management(request):
	stocks = Stock.objects.all().order_by('product')
	# products = Product.objects.all().order_by('id')
	return render(request, 'product/stock.html', {"stocks": stocks})

###############################################################
def order_management(request):
	orders = Order.objects.all().order_by('id')
	return render(request, 'customer/order.html', {"orders": orders})

###############################################################	
def purchase_management(request):
	purchases = Purchase.objects.all().order_by('id')
	return render(request, 'supply/purchase.html', {"purchases": purchases})

###############################################################
def profit_and_revenue(request):
	profits = Profit.objects.all().order_by('id')
	return render(request, 'sales/profit_and_revenue.html', {"profits": profits})
