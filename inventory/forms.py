from django import forms
from .models import Item, Transaction

# Form to handle Item creation and editing
class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'unit', 'purchase_price', 'sale_price']

    # Adding custom validation if needed
    def clean_purchase_price(self):
        purchase_price = self.cleaned_data.get('purchase_price')
        if purchase_price <= 0:
            raise forms.ValidationError("Purchase price must be greater than zero.")
        return purchase_price

    def clean_sale_price(self):
        sale_price = self.cleaned_data.get('sale_price')
        if sale_price <= 0:
            raise forms.ValidationError("Sale price must be greater than zero.")
        return sale_price

# Form to handle Transaction creation and editing
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['item', 'transaction_type', 'quantity', 'price', 'date']

    # Custom validation to ensure quantity is positive and price is valid
    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity <= 0:
            raise forms.ValidationError("Quantity must be greater than zero.")
        return quantity

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("Price must be greater than zero.")
        return price

    # Calculate amount for the transaction automatically on form submission
    def save(self, commit=True):
        transaction = super().save(commit=False)
        transaction.amount = transaction.quantity * transaction.price
        if commit:
            transaction.save()
        return transaction

from .models import Supplier, Category

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'city', 'phone_number', 'email']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']