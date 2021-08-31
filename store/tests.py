from category.models import Category
from django.test import TestCase, Client
from store.models import Product
from category.models import Category
from carts.models import Cart, CartItem
from django.core.files.uploadedfile import SimpleUploadedFile
from unittest.mock import patch

def mock_cart_id(request):
    return 1;

# Create your tests here.
class ItemRetrieveTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.image_mock = SimpleUploadedFile(
            name='test_image.jpg',
            content=open("./final_ca/static/images/logo.png", 'rb').read(), 
            content_type='image/jpeg')

        dummy_category = Category.objects.create(
            category_name = "Test Category",
            slug = "test_category"
        )

        product1 = Product.objects.create(
            category = dummy_category,
            product_name="TestProduct", 
            price=300, 
            is_available=True,
            slug="test_product",
            Images=self.image_mock,
            stock=5
        )

        product2 = Product.objects.create(
            category = dummy_category,
            product_name="TestProduct2", 
            price=149, 
            is_available=True,
            slug="test_product_2",
            Images=self.image_mock,
            stock=5
        )

        dummy_cart = Cart.objects.create(
            cart_id = 1
        )

        CartItem.objects.create(
            user = None,
            product = product1,
            cart_id = 1,
            quantity = 2,
            is_active=True
        )

        CartItem.objects.create(
            user = None,
            product = product2,
            cart_id = 1,
            quantity = 1,
            is_active=True
        )

    def test_validate_properties(self):
        '''
        Tests whether added item is visualized on
        store home page
        '''
        response = self.client.get("/store/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestProduct")
        self.assertContains(response, "300")

    @patch("carts.views._cart_id", mock_cart_id)
    def test_price_calculation(self):
        '''
        Tests tax/subtotal complex calculation of multiple
        ordered items in the shopping cart
        '''
        response = self.client.get("/cart/")
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TestProduct")
        self.assertContains(response, "TestProduct2")
        self.assertContains(response, "749")
        self.assertContains(response, "14.98")
        self.assertContains(response, "763.98") # 0.2% * (149 + 300 * 2)


