from django.test import TestCase
from django.urls import reverse

from shopapp.models import Product, Order
from shopapp.utils import add_two_nums
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Permission, User

from random import choices 
import json
ascii_letters = "qwertyuioplkjhgfdsazxcvbnm"
        
class ProductCreateViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]
    
    @classmethod
    def setUpClass(cls):
        cls.admin = User.objects.create_superuser(username="admin", password="admin")
        
    @classmethod
    def tearDownClass(cls):
        cls.admin.delete()
    
    def setUp(self) -> None:
        self.client.login(username="admin", password="admin")
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name = self.product_name).delete()
    
    def test_create_product(self):
        self.client.login(username="some_user", password="some_password")
        response = self.client.post(
            reverse("shopapp:product_create"),
            {
                "name": self.product_name,
                "price": "123.45",
                "description": "T",
                "discount": "100",
            },
            HTTP_USER_AGENT='Mozilla/5.0'
        )        
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )
        
        
class OrderDetailViewTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
    ]
    
    @classmethod
    def setUpClass(cls):
        cls.admin = User.objects.create_superuser(username="admin", password="admin")
        
    @classmethod
    def tearDownClass(cls):
        cls.admin.delete()
    
    def setUp(self) -> None:
        self.client.login(username="admin", password="admin")
        
        # создание продукта
        self.created_product = Product.objects.create(
            name="TEST_PRODUCT_NAME",
            archived = False,
            description = "...",
            price = 1,
            discount = 1,
            created_by = self.admin 
        )
        self.created_product.save()
        # создание заказа
        self.created_order = Order.objects.create(
            user=self.admin,
            promocode="ABCDEF",
            delivery_address="TEST_ORDER_ADDRESS",
        )
        self.created_order.products.set([self.created_product])
        self.created_order.save()
        self.order_pk = self.created_order.pk
        
    def tearDown(self) -> None:
        self.created_order.delete()
        self.created_product.delete()
        
    def  test_order_details(self):
        response = self.client.get(
            reverse("shopapp:order_detail", kwargs={"pk": self.order_pk}),
            HTTP_USER_AGENT='Mozilla/5.0'
        )
        order_object = response.context["object"]
        self.assertEqual( order_object.pk, self.order_pk)
        self.assertContains(response, "TEST_PRODUCT_NAME")
        self.assertContains(response, "TEST_ORDER_ADDRESS")
        

class OrderExportTestCase(TestCase):
    fixtures = [
        'products-fixture.json',
        'orders-fixture.json',
    ]
    @classmethod
    def setUpClass(cls):
        cls.admin = User.objects.create_superuser(username="admin", password="admin")
        cls.user = User.objects.create_user(username="user", password="user")
    @classmethod
    def tearDownClass(cls):
        cls.admin.delete()
        
    def test_get_orders_view(self):
        # ADMIN USER WITH STAFF RIGHTS
        self.client.login(username="admin", password="admin")
        
        response = self.client.get(
            reverse("shopapp:orders-export"),
            HTTP_USER_AGENT='Mozilla/5.0'
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.select_related("user").prefetch_related("products").order_by("pk").all()
        expected_data = [
            {
                "pk": order.pk,
                "delivery_address": order.delivery_address,
                "promocode": order.promocode,
                "user": order.user.username,
                "products":[p.pk for p in order.products]
            }
            for order in orders
        ]
        response_data = response.json()
        self.assertEqual(
            response_data["orders"],
            expected_data
        )
        self.client.logout()
    
    def test_get_orders_view_forbidden(self):    
        # SIMPLE USER WITHOUT STAFF RIGHTS
        self.client.login(username="user", password="user")
        response = self.client.get(
            reverse("shopapp:orders-export"),
            HTTP_USER_AGENT='Mozilla/5.0'
        )
        self.assertEqual(response.status_code, 403)
        self.client.logout()



























class AddTwoNumsTestCase(TestCase):
    def test_add_two_nums(self):
        result = add_two_nums(2, 3)
        self.assertEqual(result, 5, "check result = 5")
        
