from django import forms
from django.core import validators
from django.contrib.auth.models import Group

from .models import Product, Order

# class ProductForm(forms.Form):
#     name = forms.CharField(label="Name", max_length=10)
#     price = forms.DecimalField(label="Price", min_value=1, max_value=10000000, decimal_places=2)
#     description = forms.CharField(
#         label="ProductDescription",
#         widget=forms.Textarea(attrs={
#             "rows": 5,
#             "cols": 10,
#             }),
#         validators=[
#             validators.RegexValidator(
#                 regex=r"great",
#                 message="Field must contain 'great'"
#             )
#         ]
#     )
    
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "name", "price", "description", "discount", "preview"
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add the `multiple` attribute to allow selecting multiple files
        self.fields["images"].widget.attrs.update({"multiple": "true"})
        
    images = forms.ImageField(
         widget=forms.ClearableFileInput(attrs={"allow_multiple_selected": True}),
    )
        
        
class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = "user", "products", "delivery_address", "promocode", 
        widgets = {
            "delivery_address": forms.Textarea(attrs={"cols": 40, "rows": 2,}, )
        }
        labels = {
            "delivery_address": "Address",
        }
        
class GroupForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ("name",)




class CSVImportForm(forms.Form):
    csv_file = forms.FileField()