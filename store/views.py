import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Customer, Order, Product, OrderItem
from .utils import get_or_create_order_item, update_order_item_quantity
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import AnonymousUser

# Create your views here

def store(request):
    products = Product.objects.all()
    customer, created = Customer.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    context = { 'products': products, 'customer': customer, 'order': order } 
    return render(request, 'store/store.html', context)

def cart(request):
    customer, created = Customer.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    context = { 'customer': customer, 'order': order }
    return render(request, 'store/cart.html', context)

def checkout(request):
    customer, created = Customer.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    context = { 'customer': customer, 'order': order }
    return render(request, 'store/checkout.html', context)

def update_item(request):
    data = json.loads(request.body)
    product_name = data.get('product_name')
    action = data.get('action')

    customer, created = Customer.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    order_items = order.orderitem_set.all()

    order_item = get_or_create_order_item(product_name, order_items, order)
    order_item.quantity = update_order_item_quantity(action, order_item)
    
    order_item.save()
    cart_items = order.get_cart_items()
    data = {
        'cart_items': cart_items, 
        'item_quantity': order_item.quantity,
        'item_name': order_item.product.name + " quantity",
    }
    return JsonResponse(data)

def process_order(request):
    customer, created = Customer.objects.get_or_create(user=request.user if request.user.is_authenticated else None)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    order.completed = True
    order.save()

    new_order = Order.objects.create(customer=customer)
    response_data = {'message': 'Order processed successfully.'}
    return JsonResponse(response_data)
