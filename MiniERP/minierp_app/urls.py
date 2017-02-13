from django.conf.urls import url
from minierp_app import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^user_management/$', views.user_management, name='user_management'),
    url(r'^user_management/(?P<is_super>\w+)/$', views.user_management, name='user_management'),
    url(r'^customer_management/$', views.customer_management, name='customer_management'),
    url(r'^supply_management/$', views.supply_management, name='supply_management'),
    url(r'^product_management/$', views.product_management, name='product_management'),
    url(r'^stock_management/$', views.stock_management, name='stock_management'),
    url(r'^order_management/$', views.order_management, name='order_management'),
    url(r'^purchase_management/$', views.purchase_management, name='purchase_management'),
    url(r'^profit_and_revenue/$', views.profit_and_revenue, name='profit_and_revenue'),
]