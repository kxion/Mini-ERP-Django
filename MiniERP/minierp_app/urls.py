from django.conf.urls import url
from minierp_app import views
from django.contrib.auth.views import login

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^account/login/$', login, {'template_name': 'accounts/login.html'}),
    url(r'^user_management/$', views.user_management, name='user_management'),
    url(r'^user_management/(?P<is_super>\w+)/$', views.user_management, name='user_management'),
    url(r'^customer_management/$', views.customer_management, name='customer_management'),
    url(r'^customer_detail/(?P<id>[0-9]+)/$', views.customer_detail, name='customer_detail'),
    url(r'^supply_management/$', views.supply_management, name='supply_management'),
    url(r'^supply_detail/(?P<id>[0-9]+)/$', views.supply_detail, name='supply_detail'),
    url(r'^product_management/$', views.product_management, name='product_management'),
    url(r'^product_detail/(?P<id>[0-9]+)/$', views.product_detail, name='product_detail'),
    url(r'^inventory_management/$', views.inventory_management, name='inventory_management'),
    url(r'^order_management/$', views.order_management, name='order_management'),
    url(r'^purchase_management/$', views.purchase_management, name='purchase_management'),
    url(r'^purchase_order_details/(?P<id>[A-Z0-9]+)/$', views.purchase_order_details, name='purchase_order_details'),
    url(r'^add_purchase/(?P<id>[0-9]+)/$', views.add_purchase, name='add_purchase'),
    url(r'^delete_item/(?P<id>[0-9]+)/$', views.delete_item, name='delete_item'),
    url(r'^create_purchase/$', views.create_purchase, name='create_purchase'),
    url(r'^profit_and_revenue/$', views.profit_and_revenue, name='profit_and_revenue'),
]