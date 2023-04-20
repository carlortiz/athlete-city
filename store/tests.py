from django.urls import reverse
from django.test import Client, TestCase
from django.contrib.auth.models import User
from .models import Customer, Product, Order, OrderItem, ShippingAddress

# Create your tests here.


class ProductModelTestCase(TestCase):

    def setUp(self):
        product = Product.objects.create(
            name = 'Test Product',
            price = 10.99,
            image = 'test_image.webp'
        )
    
    def test_image_url_starts_with_images(self):
        test_product = Product.objects.get(name ='Test Product')
        expected_url = '/images/test_image.webp'
        self.assertEqual(test_product.image_url, expected_url)


class ProccessOrderViewTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser', 
            email='test@example.com', 
            password='testpass'
        )
        self.customer = Customer.objects.create(
            user=self.user, 
            name='Test Customer', 
            email='test@example.com'
        )
        self.product = Product.objects.create(name='Test Product', price=9.99)
        self.order = Order.objects.create(customer=self.customer, completed=False)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_process_order_creates_new_order(self):
        self.client.login(username='testuser', password='testpass')
        response = self.client.post(reverse('process-order'))
        orders = Order.objects.filter(customer=self.customer, completed=False)
        self.assertEqual(len(orders), 1)

