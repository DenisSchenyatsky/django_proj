from django.urls import path, include

from .views import (
    ShopIndexView,
    GroupsListView,
    
    ProductDetailsView, 
    ProductListView, 
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    
    OrderListView,
    OrderDetailView,
    OrderCreateView,
    OrderUpdateView,
    OrderDeleteView,
    
    OrderDataExportView,
    OrderDataExportViewById,
    
    UserOrdersListView,
)

from django.views.decorators.cache import cache_page

app_name = "shopapp"


urlpatterns = [
    #path("", cache_page(30)(ShopIndexView.as_view()), name="index"),
    path("", ShopIndexView.as_view(), name="index"),
    path("groups/", GroupsListView.as_view(), name="groups"),
    
    path("products/", ProductListView.as_view(), name="products"),   
    path("products/<int:pk>/", ProductDetailsView.as_view(), name="product_detail"),   
    path("products/create/", ProductCreateView.as_view() , name="product_create"),
    path("products/<int:pk>/update/", ProductUpdateView.as_view() , name="product_update"),
    path("products/<int:pk>/delete/", ProductDeleteView.as_view() , name="product_delete"),
    
    path("orders/", OrderListView.as_view(), name="orders"),
    path("orders/<int:pk>/", OrderDetailView.as_view(), name="order_detail"),   
    
    
    path("orders/create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/<int:pk>/update/", OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete/", OrderDeleteView.as_view(), name="order_delete"),
    
    path("orders/export/", OrderDataExportView.as_view(), name="orders-export"),
    path("orders/export/<int:pk>/user/", OrderDataExportViewById.as_view(), name="orders-export-by-id"),
    
    
    path("orders/user/<int:pk>/", UserOrdersListView.as_view(), name="orders-user"),
    
    
    
]