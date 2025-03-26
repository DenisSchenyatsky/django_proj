from django.urls import path, include

from rest_framework.routers import DefaultRouter

from .views import (
    ProductViewSet,
    OrderViewSet,
)

app_name = "shopapp_api"

routers = DefaultRouter()
routers.register("products", ProductViewSet)
routers.register("orders", OrderViewSet)

urlpatterns = [
    path("api/", include(routers.urls)),
]
