from django.contrib import admin
from django.http import HttpRequest, HttpResponse
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.urls import path

from .models import Product, Order, ProductImage
from .admin_mixins import ExportAsCSVMixin
from .forms import CSVImportForm

from .common import save_csv_products

class OrderInline(admin.TabularInline):
    model = Product.orders.through
    
class ProductImageInline(admin.StackedInline):
    model = ProductImage
    
class ProductInline(admin.StackedInline):
    model = Order.products.through


@admin.action(description="Archive/deArchive products")
def mark_archived(modeladmin: admin.ModelAdmin, request: HttpRequest, queryset: QuerySet):
    #queryset.update(archived=True)
    for obj in queryset:
        obj.archived ^= True 
        obj.save()
    
    

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin, ExportAsCSVMixin):
    change_list_template = "shopapp/products_changelist.html"
    actions = [
        mark_archived,
        "export_csv",
    ]
    inlines = [
        OrderInline,
        ProductImageInline,
        ProductInline,
    ]
    list_display = "pk", "name", "description_short", "price", "discount", "archived"
    list_display_links = "pk", "name"
    ordering = "name", "-pk" 
    search_fields = "name", "description"
    fieldsets = [
        (None, {
            "fields": ("name", "description"),
        }),
        ("Price Options", {
            "fields": ("price", "discount"),
            "classes": ("collapse", "wide",),
        }),
        ("Images", {
            "fields": ("preview", )
            
        }),
        ("Extra Options", {
            "fields": ("archived",),
            "classes": ("collapse",),
            "description": ("Extra Options Field Archived")
        }),
    ]
    
    def description_short(self, obj: Product) -> str:
        return obj.description if len(obj.description) < 48 else obj.description[:48] + "..."

    def import_csv(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            form = CSVImportForm()
            context = {
                "form": form,
            }
            return render(request, "admin/csv_form.html", context)
        #else
        form = CSVImportForm(request.POST, request.FILES)
        if not form.is_valid():
            context = {
                "form": form,
            }
            print("NOTHING WAS SAVED")
            return render(request, "admin/csv_form.html", context, status=400)
        #else
        save_csv_products(
            file = form.files["csv_file"].file,
            encoding=request.encoding
        )
        
        self.message_user(request, "Data from CSV was imported")
        
        return redirect("..")

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [
            path(
              "import-products-csv",
              self.import_csv,
              name="import_products_csv", 
            ),
        ]
        return new_urls + urls




@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [
        ProductInline,
    ]
    list_display = "delivery_address", "promocode", "created_at", "user_verbose"
    
    
    def get_queryset(self, request):
        return Order.objects.select_related("user")
    
    def user_verbose(self, obj: Order) -> str:
        return obj.user.first_name or obj.user.username
        