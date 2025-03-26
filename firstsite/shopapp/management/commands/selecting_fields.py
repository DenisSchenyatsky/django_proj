from django.core.management import BaseCommand
from django.contrib.auth.models import User
from shopapp.models import Order, Product



class Command(BaseCommand):
    """
    SELECTING
    """
    def handle(self, *args, **options):
        self.stdout.write("Start demo SELECT.")
    
        user_tuples = User.objects.values_list("username", flat=True)
        for item in user_tuples:
            self.stdout.write(str(item))
            
        product_values = Product.objects.values("pk", "name")        
        for item in product_values:
            self.stdout.write(str(item))
        
        self.stdout.write(self.style.SUCCESS("Done."))