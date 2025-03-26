from typing import Sequence
from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product

from django.db import transaction


class Command(BaseCommand):
    """
    Create order
    """
    
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write("Creating of order. Start.")
        
        user = User.objects.get(username="admin")
        
        #products: Sequence[Product] = Product.objects.defer("description", "price", "created_at").all()
        products: Sequence[Product] = Product.objects.only("id").all()
        
        
        order, created = Order.objects.get_or_create(
            delivery_address="some address",
            promocode="PROMOCODE_3",
            user=user,
        )
        #order += 1 # SPEC ERROR
        for product in products:
            order.products.add(product)
        
        order.save()
        mess = "created" if created else "exist. Passed"
        self.stdout.write(f"Order address: {order.delivery_address}, promocode: {order.promocode} {mess}")
        self.stdout.write(self.style.SUCCESS("Creating of order. Done."))