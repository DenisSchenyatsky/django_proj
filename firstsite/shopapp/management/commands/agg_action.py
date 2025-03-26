from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product
from django.db.models import Avg, Max, Min, Count, Sum



class Command(BaseCommand):
    """
    AGGREGATE
    """
    def handle(self, *args, **options):
        self.stdout.write("Start BULK DEMO.")
        
        res = Product.objects.filter(
                name__contains="Smartphone",
            ).aggregate(
                v1=Avg("price"),
                v2=Max("price"),
                v3=Min("price"),
                v4=Count("price"),
            )
        print(res)
        for key, value in res.items():
            print(key, ":", value)
            
        res = Order.objects.annotate(
            total=Sum("products__price", default=0),
            products_count=Count("products"),
        )
        for obj in res:
            print(f"N`{obj.id}"
                  f" with {obj.products_count}"
                  f" products worth {obj.total}"
            )
    
        self.stdout.write(self.style.SUCCESS("Done."))