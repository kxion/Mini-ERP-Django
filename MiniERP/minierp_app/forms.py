# gig form setting
from django.forms import ModelForm, ModelChoiceField
from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import Customer, Supply, Product, Inventory

class CustomerForm(ModelForm):
    class Meta:
        model = Customer
        fields = ['company_name', 'contact_name', 'address', 'city', 'state', 'zip_code', 'phone', 'fax', 'email']
    def __init__(self, *args, **kwargs):
        super(CustomerForm, self).__init__(*args, **kwargs)
        self.fields['state'].widget.attrs['style'] = "width:122.25px"
        self.fields['email'].widget.attrs['style'] = "width:132%"


class SupplyForm(ModelForm):
    class Meta:
        model = Supply
        fields = ['company_name', 'contact_name', 'address', 'city', 'state', 'zip_code', 'phone', 'fax', 'email']
    def __init__(self, *args, **kwargs):
        super(SupplyForm, self).__init__(*args, **kwargs)
        self.fields['state'].widget.attrs['style'] = "width:122.25px"
        self.fields['email'].widget.attrs['style'] = "width:132%"
       

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['supplier', 'name', 'model', 'dimention', 'weight', 'price', 'photo', 'note']
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['supplier'].widget.attrs['style'] = "width:195.59px"
        
        
class AmountForm(forms.Form):
    amount = forms.IntegerField(validators=[MinValueValidator(1)])

class CustomerSelectForm(forms.Form):
    customer = ModelChoiceField(queryset=Customer.objects.all())
    def __init__(self, *args, **kwargs):
        super(CustomerSelectForm, self).__init__(*args, **kwargs)
        self.fields['customer'].widget.attrs['style'] = "width:230px"
