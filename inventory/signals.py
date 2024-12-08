from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from inventory.models import Supplier, Category, Item, Transaction, StockBalance
from inventory.kafka_producer import publish_message
from django.db.models import Sum

# Handle Supplier CRUD Events
@receiver(post_save, sender=Supplier)
def handle_supplier_save(sender, instance, created, **kwargs):
    event = "CREATE" if created else "UPDATE"
    message = {
        'model': 'Supplier',
        'event': event,
        'data': {
            'id': instance.id,
            'name': instance.name,
            'city': instance.city,
            'phone_number': instance.phone_number,
            'email': instance.email
        }
    }
    publish_message('inventory_topic', message)

@receiver(post_delete, sender=Supplier)
def handle_supplier_delete(sender, instance, **kwargs):
    message = {
        'model': 'Supplier',
        'event': 'DELETE',
        'data': {
            'id': instance.id,
            'name': instance.name,
        }
    }
    publish_message('inventory_topic', message)

# Handle Category CRUD Events
@receiver(post_save, sender=Category)
def handle_category_save(sender, instance, created, **kwargs):
    event = "CREATE" if created else "UPDATE"
    message = {
        'model': 'Category',
        'event': event,
        'data': {
            'id': instance.id,
            'name': instance.name,
        }
    }
    publish_message('inventory_topic', message)

@receiver(post_delete, sender=Category)
def handle_category_delete(sender, instance, **kwargs):
    message = {
        'model': 'Category',
        'event': 'DELETE',
        'data': {
            'id': instance.id,
            'name': instance.name,
        }
    }
    publish_message('inventory_topic', message)

# Handle Item CRUD Events
@receiver(post_save, sender=Item)
def handle_item_save(sender, instance, created, **kwargs):
    event = "CREATE" if created else "UPDATE"
    message = {
        'model': 'Item',
        'event': event,
        'data': {
            'id': instance.id,
            'name': instance.name,
            'supplier_id': instance.supplier.id if instance.supplier else None,
            'category_id': instance.category.id if instance.category else None,
            'unit': instance.unit,
            'purchase_price': str(instance.purchase_price),
            'sale_price': str(instance.sale_price),
        }
    }
    publish_message('inventory_topic', message)

@receiver(post_delete, sender=Item)
def handle_item_delete(sender, instance, **kwargs):
    message = {
        'model': 'Item',
        'event': 'DELETE',
        'data': {
            'id': instance.id,
            'name': instance.name,
        }
    }
    publish_message('inventory_topic', message)

# Handle Transaction CRUD Events
@receiver(post_save, sender=Transaction)
def handle_transaction_save(sender, instance, created, **kwargs):
    event = "CREATE" if created else "UPDATE"
    message = {
        'model': 'Transaction',
        'event': event,
        'data': {
            'id': instance.id,
            'item_id': instance.item.id,
            'transaction_type': instance.transaction_type,
            'quantity': instance.quantity,
            'price': str(instance.price),
            'date': instance.date.strftime('%Y-%m-%d'),
            'profit': str(instance.profit) if instance.profit else None,
        }
    }
    publish_message('inventory_topic', message)

    # Update stock balance
    update_stock_balance(instance.item)

@receiver(post_delete, sender=Transaction)
def handle_transaction_delete(sender, instance, **kwargs):
    message = {
        'model': 'Transaction',
        'event': 'DELETE',
        'data': {
            'id': instance.id,
            'item_id': instance.item.id,
        }
    }
    publish_message('inventory_topic', message)

    # Update stock balance
    update_stock_balance(instance.item)

# Update StockBalance
def update_stock_balance(item):
    stock_in_total = Transaction.objects.filter(item=item, transaction_type='stock_in').aggregate(Sum('quantity'))['quantity__sum'] or 0
    stock_out_total = Transaction.objects.filter(item=item, transaction_type='stock_out').aggregate(Sum('quantity'))['quantity__sum'] or 0

    stock_balance, created = StockBalance.objects.get_or_create(item=item)
    stock_balance.item_balance = stock_in_total - stock_out_total
    stock_balance.save()

    # Publish stock balance update message
    message = {
        'model': 'StockBalance',
        'event': 'UPDATE',
        'data': {
            'item_id': item.id,
            'item_balance': stock_balance.item_balance,
        }
    }
    publish_message('inventory_topic', message)
