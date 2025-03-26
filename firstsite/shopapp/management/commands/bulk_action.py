from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product



class Command(BaseCommand):
    """
    BULK
    """
    def handle(self, *args, **options):
        self.stdout.write("Start BULK DEMO.")
        
        res = Product.objects.filter(
            name__contains="Smartphone",
        ).update(discount=10)
        
        print(res)
        # info = [
        #     ('Smartphone 1', 199),
        #     ('Smartphone 2', 299),
        #     ('Smartphone 3', 399),
        # ]
        # products = [
        #     Product(name=name, price=price)
        #     for name, price in info
        # ]
        
        # res = Product.objects.bulk_create(products)
        
        # for obj in res:
        #     print(obj)
    
        self.stdout.write(self.style.SUCCESS("Done."))