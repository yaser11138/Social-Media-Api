from ..models import Product


def create_product(name: str) -> Product:
    product = Product.objects.create(name=name)
    return product
