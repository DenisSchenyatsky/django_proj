from django.core.management import BaseCommand

from shopapp.models import Product

class Command(BaseCommand):
    """
    Creates product
    """
    
    def handle(self, *args, **options):
        self.stdout.write("Creating of products. Start.")
        
        p_n_d = (
            ("Laptop", "..."),
            ("Desktop","ABCDEF"),
            ("Prostokwasha", "xyzzyx"),
        )
        for p_n, p_d in p_n_d:
            product, created = Product.objects.get_or_create(name=p_n, description=p_d)
            mess = "was created" if created else "exist. Passed."
            self.stdout.write(f"Product: {product.name}: '{product.description}' {mess}")
            
        self.stdout.write(self.style.SUCCESS("Creating of products. Done."))
        