from django.test import TestCase
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


# Write a test to make sure that process order leaves only one active order at a time,
# otherwise it would produce an error
