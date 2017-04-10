# gig form setting
from django.forms import ModelForm
from .models import Customer, Supply, Product, Inventory, Order, Purchase, Profit, ProductModel

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['company_name', 'contact_name', 'address', 'city', 'state', 'zip_code', 'phone', 'fax', 'note']
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['state'].widget.attrs['style'] = "width:122.25px"
        self.fields['note'].widget.attrs['style'] = "width:132%"


class SupplyForm(ModelForm):
    class Meta:
        model = Supply
        fields = ['company_name', 'contact_name', 'address', 'city', 'state', 'zip_code', 'phone', 'fax', 'note']
    def __init__(self, *args, **kwargs):
        super(SupplyForm, self).__init__(*args, **kwargs)
        self.fields['state'].widget.attrs['style'] = "width:122.25px"
        self.fields['note'].widget.attrs['style'] = "width:132%"
       

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['supplier', 'name', 'model', 'dimention', 'weight', 'price', 'photo', 'note']
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].widget.attrs['style'] = "width:195.59px"
        # self.fields['photo'].widget.attrs['style'] = "height:34px"
        

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['customer', 'product', 'product_amount', 'note']

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['style'] = "width:230px"
        self.fields['product'].queryset = Product.objects.filter().order_by('name')
        self.fields['customer'].widget.attrs['style'] = "width:200px"
        self.fields['customer'].queryset = Customer.objects.filter().order_by('company_name')
        self.fields['note'].widget.attrs['style'] = "width:128%"

class PurchaseForm(ModelForm):
    class Meta:
        model = Purchase
        fields = ['product', 'product_amount', 'note']
        
    def __init__(self, *args, **kwargs):
        super(PurchaseForm, self).__init__(*args, **kwargs)
        self.fields['product'].widget.attrs['style'] = "width:230px"
        # self.fields['product'].widget.attrs['style'] = "color:red"
        self.fields['product'].widget.attrs['id'] = "abc123"
        self.fields['product'].queryset = Product.objects.filter().order_by('name')
        self.fields['note'].widget.attrs['style'] = "width:97%"
        # self.fields['model'].widget.attrs['style'] = "width:200px"
        # self.fields['model'].queryset = ProductModel.objects.filter().exclude(product_model="None")
        
# instance = getattr(self, 'instance', None)
#         if instance and instance.pk:
#         if instance.name is not None:
#             self.fields['name'].widget.attrs['readonly'] = True

# class StockForm(ModelForm):
#     class Meta:
#         model = Stock
#         fields = ['product', 'note', 'purchase', 'sell']

# class ProfitForm(ModelForm):
#     class Meta:
#         model = Profit
#         fields = ['order_number', 'purchase_number', 'note']

