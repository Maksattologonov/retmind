from .models import Product, Tag, Category
from common.exceptions import ObjectNotFoundException


class ProductService:
    model = Product
    tag_model = Tag
    category_model = Category

    @classmethod
    def get_product(cls, **filters):
        try:
            print(cls.model.objects.filter(**filters))
            return cls.model.objects.filter(**filters)
        except cls.model.DoesNotExist:
            raise ObjectNotFoundException('Product not found')

