"""
Модуль взаимодействия.

Представлений и orm-моделей бд.

Вот.
"""



from timeit import default_timer
from csv import DictWriter

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.views import View
from django.views.generic import (
    #TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser

from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

from drf_spectacular.utils import extend_schema, OpenApiResponse


from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

from django.core.cache import cache

from .models import Product, Order, User, ProductImage
from .forms import ProductForm, OrderForm, GroupForm

from .common import save_csv_products

from .serializers import ProductSerializer, OrderSerializer

import random
import logging

log  = logging.getLogger(__name__)






@extend_schema(description="Product wievs CURD")
class ProductViewSet(ModelViewSet):
    """
    Набор представлений CRUD для Product.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = [
        "name", 
        "description",
    ]
    filterset_fields = [
        "name",
        "description",
        "price",
        "discount",
        "archived",
    ]
    ordering_fields = [
        "pk",
        "name",
        "price",
        "discount",
    ]
    
    # Это нужно, чтобы в swagger отплевывало надпись ниже
    @extend_schema(
        summary="Get 1 product by ID",
        description="Retrieves **Product**, return 404 if None.",
        responses={
            200: ProductSerializer,
            404: OpenApiResponse(description=" NOT FOUND ")
        }
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)
    
    @action(methods=["get"], detail=False)
    def download_csv(self, request: Request):
        
        response = HttpResponse(content_type="text/csv")
        filename = "products-export.csv"
        response["Content-Disposition"] = f"attachment; filename={filename}"
        
        queryset = self.filter_queryset(self.get_queryset())
        fields = [
        "name",
        "description",
        "price",
        "discount",
        ]
        queryset = queryset.only(*fields)
        writer = DictWriter(response, fieldnames=fields)
        writer.writeheader()
        
        for product in queryset:
            writer.writerow({
                field: getattr(product, field)
                for field in fields
            })    
            
        return response
    
    @action(detail=False, methods=["post"], parser_classes=[MultiPartParser])
    def upload_csv(self, request: Request):
        products = save_csv_products(
            file=request.FILES["file"].file,
            encoding=request.encoding
        )
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data)
    
    @method_decorator(cache_page(30))
    def list(self, *args, **kwargs):
        print('*'*8, "********************", '*'*8)
        print('*'*8, "FUNC LIST IS EXECUTE", '*'*8)
        print('*'*8, "********************", '*'*8)
        return super().list(*args, **kwargs)
        
    
class OrderViewSet(ModelViewSet):
    queryset = Order.objects.prefetch_related("products").all()
    serializer_class = OrderSerializer
    filter_backends = [
        SearchFilter,
        DjangoFilterBackend,
        OrderingFilter,
    ]
    search_fields = (
            "delivery_address",
            "promocode", 
        )
    filterset_fields = (
            "delivery_address",
            "promocode", 
            "user",
            "products",
            
        )
    ordering_fields = (
            "pk",
            "delivery_address",
            "promocode", 
            "created_at",
        )
    



class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        tups_of_vals = (
            ('First', 1234),
            ('Second', 4321),
            ('Third', 12345),
        ) if random.randint(0, 1) else ()
        
        context = {
            "time_running": default_timer(),
            "some_list": tups_of_vals,        
            "some_str": "abc\ndef\nghkl",
        }
        log.debug("Products for shop index: %s", tups_of_vals)
        log.info("Rendering shop index")
        
        print('*'*8, '**********************************************', '*'*8)
        print('*'*8, 'SHOP INDEX CONTEXT:', context, '*'*8)
        print('*'*8, '**********************************************', '*'*8)
        
        return render(request, 'shopapp/shop-index.html', context=context)

class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            "form": GroupForm(),
            "groups": Group.objects.prefetch_related('permissions').all()
        }
        return render(request, 'shopapp/groups-list.html', context=context)
    
    def post(self, request: HttpRequest) -> HttpResponse:
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()            
        return redirect(request.path)





class OrderListView(LoginRequiredMixin, ListView):
    template_name = "shopapp/orders-list.html"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )    

class OrderDetailView(PermissionRequiredMixin, DetailView):
    permission_required = "shopapp.view_order"
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )

class OrderCreateView(CreateView):
    model = Order
    fields = (
        "delivery_address", 
        "promocode", 
        "user", 
        "products"
    )
    success_url = reverse_lazy("shopapp:orders")

class OrderUpdateView(UpdateView):
    model = Order
    fields = (
        "delivery_address", 
        "promocode", 
        "user", 
        "products"
    )
    #queryset = model.objects.filter(products__archived=False).prefetch_related()#.all()
    template_name_suffix = "_update_form"
    
    def get_success_url(self): # Для возможности перенаправить по url с индексом pk
        return reverse(
            "shopapp:order_detail",
            kwargs = {"pk": self.object.pk}
        )


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy("shopapp:orders")    



class ProductListView(ListView):
    template_name = "shopapp/products-list.html"
    model = Product
    queryset = Product.all_objects.all() # !!! objects переопределен
    context_object_name = "products"

class ProductDetailsView(DetailView):
    template_name = "shopapp/product_detail.html"
    #model = Product
    queryset = Product.objects.prefetch_related("images")
    fields = "name", "price", "description", "discount", "preview"
    context_object_name = "product"

class ProductCreateView(UserPassesTestMixin, CreateView):
    # создавать только если есть разрешение
    def test_func(self):
        return self.request.user.has_perm('shopapp.add_product') 
    
    # приматывание user к таблице
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(ProductCreateView, self).form_valid(form)
    
    model = Product
    fields = "name", "price", "description", "discount", "preview"
    success_url = reverse_lazy("shopapp:products")

class ProductUpdateView(UserPassesTestMixin, UpdateView):
    # изменять только если есть разрешение
    def test_func(self):
        return self.request.user.has_perm('shopapp.change_product') 
    
    model = Product
    #fields = "name", "price", "description", "discount", "preview"
    template_name_suffix = "_update_form"
    #success_url = reverse_lazy("shopapp:products")
    form_class = ProductForm
    
    def get_success_url(self):
        return reverse(
            "shopapp:product_detail",
            kwargs = {"pk": self.object.pk}
        )
        
    def form_valid(self, form):
        # Проверка на наличие разрешения
        obj = form.save(commit=False)
        if self.request.user.is_superuser or (obj.created_by == self.request.user):
            response = super().form_valid(form)
            for image in form.files.getlist("images"):
                ProductImage.objects.create(
                    product=self.object,
                    image=image,
                )
            return response
        #else
        return super(ProductUpdateView, self).form_invalid(form)
        
                

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy("shopapp:products")    

    # Удаление понарошку
    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)





# Задание 19 кэширование в html-шаблоне orders-user-list.html
# http://127.0.0.1:8000/ru/shop/orders/user/1/

class UserOrdersListView(LoginRequiredMixin, ListView):
    
    template_name = "shopapp/orders-user-list.html"
    
    def get_queryset(self):         
        return (
            Order.objects
            .select_related("user")
            .filter(user__pk=self.kwargs['pk'])
            .prefetch_related("products")
        )    


class OrderDataExportView(UserPassesTestMixin, View):    
    def test_func(self):
        return self.request.user.has_perm('shopapp.is_staff')
        
    def get(self, request: HttpRequest) -> JsonResponse:        
        orders = Order.objects.select_related("user").prefetch_related("products").order_by("pk").all()
        
        data =[]           
        for order in orders:
            ser = OrderSerializer(instance=order)
            data.append(ser.data)
            
        return JsonResponse({"orders": data})

# Задание 19 кэширование на "низком уровне", т.е. в функции-обработчике http запроса
# http://127.0.0.1:8000/ru/shop/orders/export/7/user/

class OrderDataExportViewById(LoginRequiredMixin, View):    
    def get(self, request: HttpRequest, *args, **kwargs) -> JsonResponse: 
        pk = kwargs.get('pk', None)
        
        if pk:
            cache_key = f"order_data_pk_depends{pk}"
            data = cache.get(cache_key)
            if data is None:
                data = []
                orders = (
                    Order.objects
                    .select_related("user")
                    .filter(user__pk=pk)
                    .prefetch_related("products")
                    .order_by("pk").all())            
            
                data = [
                    OrderSerializer(instance=order).data
                    for order in orders
                ]
                # check & demo
                data.append({"CHECK_CACHE_DEMO:": random.random()})
                cache.set(cache_key, data, 20)                                    
            return JsonResponse({"orders": data})
        #else    
        return JsonResponse({"Sorry": "Nothing to show"})

