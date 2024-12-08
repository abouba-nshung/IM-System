from django.db import models
from django.utils.timezone import now

# Supplier Model
class Supplier(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Item model to represent each inventory item
class Item(models.Model):
    name = models.CharField(max_length=100)  # Name of the item
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.CharField(max_length=50)   # Unit of measurement (e.g., pieces, kg, etc.)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2)  # Purchase price per unit
    sale_price = models.DecimalField(max_digits=10, decimal_places=2)     # Sale price per unit
    

    def __str__(self):
        return self.name


class Transaction(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=[('stock_in', 'Stock In'), ('stock_out', 'Stock Out')])
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    profit = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Profit field
    
    def __str__(self):
        return f"{self.item.name} - {self.transaction_type} - {self.date}"
"""
from django.db.models import Sum
class StockBalance(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE, related_name='stock_balance')
    item_balance = models.IntegerField(default=0)

    def update_balance(self):
        # Calculate stock balance from transactions
        stock_in = Transaction.objects.filter(item=self.item, transaction_type='stock_in').aggregate(
            total_in=Sum('quantity')
        )['total_in'] or 0

        stock_out = Transaction.objects.filter(item=self.item, transaction_type='stock_out').aggregate(
            total_out=Sum('quantity')
        )['total_out'] or 0

        self.item_balance = stock_in - stock_out
        self.save()

    def __str__(self):
        return f"{self.item.name} - Balance: {self.item_balance}"
    
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Sum

class StockBalance(models.Model):
    item = models.OneToOneField(Item, on_delete=models.CASCADE)
    item_balance = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.item.name} - Balance: {self.item_balance}"

# Signals to update StockBalance
@receiver(post_save, sender=Transaction)
def update_stock_balance_on_save(sender, instance, **kwargs):
    item = instance.item
    stock_in_total = Transaction.objects.filter(item=item, transaction_type='stock_in').aggregate(Sum('quantity'))['quantity__sum'] or 0
    stock_out_total = Transaction.objects.filter(item=item, transaction_type='stock_out').aggregate(Sum('quantity'))['quantity__sum'] or 0

    stock_balance, created = StockBalance.objects.get_or_create(item=item)
    stock_balance.item_balance = stock_in_total - stock_out_total
    stock_balance.save()

@receiver(post_delete, sender=Transaction)
def update_stock_balance_on_delete(sender, instance, **kwargs):
    item = instance.item
    stock_in_total = Transaction.objects.filter(item=item, transaction_type='stock_in').aggregate(Sum('quantity'))['quantity__sum'] or 0
    stock_out_total = Transaction.objects.filter(item=item, transaction_type='stock_out').aggregate(Sum('quantity'))['quantity__sum'] or 0

    stock_balance, created = StockBalance.objects.get_or_create(item=item)
    stock_balance.item_balance = stock_in_total - stock_out_total
    stock_balance.save()


