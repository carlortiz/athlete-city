from django.test import Client, TestCase
from .models import Customer, Product, Order, OrderItem, ShippingAddress

# Create your tests here.

# Very important, do not publish before doing this
# Write tests for bugs that should NEVER occur
# Use exceptions to check for more typical errors
# Go around the important functions and features and what not and make sure that you are
# using defensive programming

class ProductModelTestCase(TestCase):
    
    def test_image_url_starts_with_images(self):
        product = Product.objects.create(
            name = 'Test Product',
            price = 10.99,
            image = 'test_image.webp'
        )

        expected_url = '/images/test_image.webp'
        self.assertEqual(product.image_url, expected_url)


class ProcessOrderViewTestCase(TestCase):

    '''
        def setUp(self):
            self.client = Client()
            self.user = User.objects.create_user(
                username='testuser', email='testuser@example.com', password='testpass')
            self.customer = Customer.objects.create(user=self.user)
            self.order1 = Order.objects.create(customer=self.customer, completed=False)
            self.order2 = Order.objects.create(customer=self.customer, completed=False)

        def test_process_order(self):
        # Login as the test user
        self.client.login(username='testuser', password='testpass')

        # Send a POST request to the process_order view
        response = self.client.post(reverse('process_order'))

        # Check that there is only one Order object with completed=False
        orders = Order.objects.filter(customer=self.customer, completed=False)
        self.assertEqual(len(orders), 1)
        self.assertEqual(orders[0], self.order2)
    '''


# Write a test to make sure that process order leaves only one active order at a time,
# otherwise it would produce an error
