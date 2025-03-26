
from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product


class Command(BaseCommand):
    """
    Create order
    """
    
    def handle(self, *args, **options):
        self.stdout.write("Updating of order. Start.")
        
        if not (order:=Order.objects.first()):
            self.stdout.write("Order were not found.")
            return
        
        products = Product.objects.all()
        for product in products:
            order.products.add(product)
        
        order.save()
        
        self.stdout.write(self.style.SUCCESS("Updating of order. Done."))