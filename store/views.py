import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .models import Customer, Order, Product, OrderItem

# Create your views here


def store(request):
    products = Product.objects.all()
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    context = { 'products': products, 'customer': customer, 'order': order } 
    return render(request, 'store/store.html', context)


def cart(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    context = { 'customer': customer, 'order': order}

    return render(request, 'store/cart.html', context)


def checkout(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    context = { 'customer': customer, 'order': order}
    return render(request, 'store/checkout.html', context)


def update_item(request):
    data = json.loads(request.body)
    product_name = data.get('product_name')

    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)
    order_items = order.orderitem_set.all()

    # finds the order item with a product name that matches the product name above
    order_item = order_items.filter(product__name=product_name).first()
    if order_item:
        order_item.quantity += 1
        order_item.save()
    else: 
        product = Product.objects.get(name=product_name)
        order_item = OrderItem.objects.create(order=order, product=product, quantity=1)

    cart_items = order.get_cart_items()

    data = {
        'message': 'Quantity updated.',
        'cart_items': cart_items,
    }

    return JsonResponse(data)


def process_order(request):
    customer, created = Customer.objects.get_or_create(user=request.user)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    order.completed = True
    order.save()

    new_order = Order.objects.create(customer=customer)

    response_data = {
        'message': 'Order processed successfully.'
    }

    return JsonResponse(response_data)
