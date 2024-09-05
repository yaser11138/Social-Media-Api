from django.db.models import QuerySet
from ..models import Product


def get_products() -> QuerySet :
    return Product.objects.all()