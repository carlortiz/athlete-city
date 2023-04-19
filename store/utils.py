# utils.py

from .models import Customer, Product, Order, OrderItem, ShippingAddress

def get_or_create_order_item(product_name, order_items, order):
    order_item = order_items.filter(product__name=product_name).first()
    if not order_item:
        product = Product.objects.get(name=product_name)
        order_item = OrderItem.objects.create(order=order, product=product, quantity=1)
    
    return order_item

def update_order_item_quantity(action, order_item):
    if action == "add":
        order_item.quantity += 1
    else:
        order_item.quantity -= 1
    return order_item.quantity