from django.contrib.auth.models import User
from django.db import models

def product_preview_directory_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/preview/{filename}".format(
        pk=instance.pk,
        filename=filename,
    )
    
def product_images_directory_path(instance: "Product", filename: str) -> str:
    return "products/product_{pk}/images/{filename}".format(
        pk=instance.product.pk,
        filename=filename,
    )


class CustomProductManager(models.Manager):
    use_for_related_fields = True
    def get_queryset(self):
        return super().get_queryset().filter(archived=False)
    
class Product(models.Model):
    """
    Модель Product.
    
    Объект описывающий товар, который можно приобрести в магазине. (shop)
    
    Посмотреть заказы: :model:`shopapp.Order`
    """
    objects = models.Manager()
    all_objects = CustomProductManager()
   
    class Meta:
        ordering = ["name", "price"]
        base_manager_name = 'objects'
        
    name = models.CharField(max_length=100, db_index=True)
    description = models.TextField(null=False, blank=True, db_index=True)
    price = models.DecimalField(default=0, max_digits=8, decimal_places=2)
    discount = models.SmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)
    
    # нельзя удалять пользователя при наличии продуктов им внесёнными
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, null=True) 
    
    preview = models.ImageField(null=True, blank=True, upload_to=product_preview_directory_path)
    
    def __str__(self) -> str:
        return f"Product(pk={self.pk}, name={self.name!r})"
    
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=product_images_directory_path)
    description = models.CharField(max_length=200, null=False, blank=True)
    
    
class Order(models.Model):
    """
    Заказы. (покупки)
    
    
    """
    delivery_address = models.TextField(null=False, blank=True)
    promocode = models.CharField(max_length=20, null=False, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    
    products = models.ManyToManyField(Product, related_name="orders")
    
    receipt = models.FileField(null=True, upload_to='orders/receipts')