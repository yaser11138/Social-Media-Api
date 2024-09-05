from django.urls import path
from .api.product import ProductView


urlpatterns = [
    path("product", ProductView.as_view(),  name="product")
]