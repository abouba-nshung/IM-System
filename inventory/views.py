from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Sum
from .models import Item, Transaction
from .forms import ItemForm, TransactionForm
from django.utils.timezone import now


# from django.contrib.auth.decorators import login_required
# Item views
def item_list(request):
    items = Item.objects.all()
    return render(request, 'item_list.html', {'items': items})


def add_item(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})


def edit_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        form = ItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ItemForm(instance=item)
    return render(request, 'edit_item.html', {'form': form, 'item': item})


def delete_item(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'delete_item.html', {'item': item})


# Transaction views
def transaction_list(request):
    transactions = Transaction.objects.all()
    return render(request, 'transaction_list.html', {'transactions': transactions})


def add_item(request):
    if request.method == "POST":
        form = ItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('items')
    else:
        form = ItemForm()
    return render(request, 'add_item.html', {'form': form})


def transactions(request):
    # Replace with your logic to fetch transactions
    return render(request, 'transactions.html', {})

from django.core.paginator import Paginator

def transaction_list(request):
    # Fetch all transactions and calculate total for each transaction dynamically
    transactions = Transaction.objects.all()
    for transaction in transactions:
        transaction.total = transaction.quantity * transaction.price  # Add total attribute

    # Set up pagination: 10 transactions per page
    paginator = Paginator(transactions, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'transaction_list.html', {'page_obj': page_obj})

from django.shortcuts import render, redirect
from .models import Item, Transaction

from datetime import datetime
from django.shortcuts import render, redirect
from .models import Item, Transaction

def add_transaction(request):
    if request.method == 'POST':
        item_id = request.POST.get('item')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        date_str = request.POST.get('date')  # Get the date as a string
        transaction_type = request.POST.get('transaction_type')

        # Convert quantity and price to the correct data types
        quantity = int(quantity)
        price = float(price)

        # Convert the date string to a datetime.date object
        if date_str:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()  # Convert to datetime.date

        # Fetch the selected item
        item = Item.objects.get(id=item_id)

        # Initialize profit as None (will be calculated only for Stock Out)
        profit = 0

        # Calculate profit only for Stock Out
        if transaction_type == 'stock_out':
            purchase_price = item.purchase_price
            sale_price = item.sale_price
            profit = (sale_price * quantity) - (purchase_price * quantity)

        # Create a new transaction
        Transaction.objects.create(
            item=item,
            quantity=quantity,
            price=price,
            date=date_obj,  # Store the datetime.date object
            transaction_type=transaction_type,
            profit=profit  # Store the calculated profit for Stock Out transactions
        )
        # messages.success(request, f"Transaction recorded successfully for {item.name}!")
        return redirect('transaction_list')

    # Get all items for the form
    items = Item.objects.all()
    return render(request, 'add_transaction.html', {'items': items})


from django.shortcuts import get_object_or_404

def edit_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == 'POST':
        item_id = request.POST.get('item')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        date = request.POST.get('date')
        transaction_type = request.POST.get('transaction_type')

        # Fetch the selected item
        item = Item.objects.get(id=item_id)

        # Update transaction
        transaction.item = item
        transaction.quantity = int(quantity)
        transaction.price = float(price)
        transaction.date = date
        transaction.transaction_type = transaction_type

        # Save the updated transaction
        transaction.save()
        return redirect('transaction_list')

    items = Item.objects.all()
    return render(request, 'edit_transaction.html', {
        'transaction': transaction,
        'items': items,
    })


def delete_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)

    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')

    return render(request, 'delete_transaction.html', {'transaction': transaction})



from .models import StockBalance


def stock_balance_view(request):
    stock_balances = StockBalance.objects.select_related('item').all()
    return render(request, 'stock_balance.html', {'stock_balances': stock_balances})


from django.shortcuts import render, redirect, get_object_or_404
from .models import Supplier, Category, Item
from .forms import SupplierForm, CategoryForm  # Assume you have forms for Supplier and Category.


# Supplier Views
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'supplier_list.html', {'suppliers': suppliers})


def add_supplier(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    return render(request, 'add_supplier.html', {'form': form})


def edit_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            return redirect('supplier_list')
    else:
        form = SupplierForm(instance=supplier)
    return render(request, 'edit_supplier.html', {'form': form})


def delete_supplier(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.delete()
        return redirect('supplier_list')
    return render(request, 'delete_supplier.html', {'supplier': supplier})


# Category Views
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})


def edit_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'edit_category.html', {'form': form})


def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'delete_category.html', {'category': category})


from django.shortcuts import render, redirect
from .models import Item, Supplier, Category


def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('item_name')
        unit = request.POST.get('unit')
        purchase_price = request.POST.get('purchase_price')
        sale_price = request.POST.get('sale_price')
        supplier_id = request.POST.get('supplier')
        category_id = request.POST.get('category')

        # Fetch the supplier and category
        supplier = Supplier.objects.get(id=supplier_id)
        category = Category.objects.get(id=category_id)

        # Save the new item
        Item.objects.create(
            name=name,
            unit=unit,
            purchase_price=purchase_price,
            sale_price=sale_price,
            supplier=supplier,
            category=category
        )
        return redirect('item_list')

    # Pass suppliers and categories to the template
    suppliers = Supplier.objects.all()
    categories = Category.objects.all()

    return render(request, 'add_item.html', {
        'suppliers': suppliers,
        'categories': categories
    })


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# Login View
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')  # Redirect to dashboard after successful login
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'login.html')


# Logout View
def user_logout(request):
    logout(request)
    return redirect('login')  # Redirect to login page after logout


# Example: Protect dashboard with login_required
# from django.db.models import Sum

from django.db.models import Sum, F, Q, Value as V
from django.db.models.functions import Coalesce  # Import Coalesce
from datetime import datetime
from hdfs import InsecureClient
from collections import defaultdict
# HDFS Configuration
HDFS_URL = 'http://localhost:9870'
HDFS_USER = 'hdfs'
OUTPUT_FILE = '/stock_analysis/output/result.txt'

client = InsecureClient(HDFS_URL, user=HDFS_USER)

@login_required
def dashboard(request):
    # Get date range from the request
    start_date = request.GET.get('start_date', None)
    end_date = request.GET.get('end_date', None)

    # Convert to datetime objects if provided
    try:
        if start_date:
            start_date = datetime.strptime(start_date, '%Y-%m-%d')
        if end_date:
            end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        start_date, end_date = None, None

    # Filter transactions by date range if dates are provided
    date_filter = Q()
    if start_date:
        date_filter &= Q(date__gte=start_date)
    if end_date:
        date_filter &= Q(date__lte=end_date)

    # Aggregate purchase value from "Stock IN" transactions
    purchase_value = (
        Transaction.objects.filter(transaction_type="stock_in")
        .filter(date_filter)
        .aggregate(total_sales=Sum(F('price') * F('quantity')))['total_sales'] or 0
    )

    # Aggregate sales value from "Stock OUT" transactions
    sales_value = (
        Transaction.objects.filter(transaction_type="stock_out")
        .filter(date_filter)
        .aggregate(total_sales=Sum(F('price') * F('quantity')))['total_sales'] or 0
    )

    # Aggregate total profit from all transactions
    total_profit = (
        Transaction.objects.filter(date_filter)
        .aggregate(Sum('profit'))['profit__sum'] or 0
    )

    # Calculate the number of items purchased, sold, and balance (using item name)
    items_data = (
        Transaction.objects.filter(date_filter)
        .values('item__name')  # Fetch item names instead of IDs
        .annotate(
            purchased=Coalesce(Sum('quantity', filter=Q(transaction_type="stock_in")), V(0)),
            sold=Coalesce(Sum('quantity', filter=Q(transaction_type="stock_out")), V(0)),
        )
        .annotate(balance=F('purchased') - F('sold'))  # Calculate balance
    )

    # Fetch MapReduce results from HDFS
    mapreduce_results = []
    try:
        with client.read(OUTPUT_FILE, encoding='utf-8') as reader:
            lines = reader.readlines()[1:]  # Skip the header line
            for line in lines:
                item, total, profit = line.strip().split("\t")
                mapreduce_results.append({
                    "item": item,
                    "total": float(total),
                    "profit": float(profit),
                })
    except Exception as e:
        print(f"Error reading MapReduce results: {e}")
        mapreduce_results = None

    # Pass all data to the template
    context = {
        'purchase_value': purchase_value,
        'sales_value': sales_value,
        'total_profit': total_profit,
        'items_data': items_data,
        'mapreduce_results': mapreduce_results,
        'start_date': start_date.strftime('%Y-%m-%d') if start_date else '',
        'end_date': end_date.strftime('%Y-%m-%d') if end_date else '',
    }
    return render(request, 'dashboard.html', context)

