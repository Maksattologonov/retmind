from django.shortcuts import render
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from .models import Product
from .serializers import ProductSerializer
from .services import ProductService
from django.http import HttpResponse
from openpyxl import Workbook


class ProductListAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = [JWTAuthentication]

    def get(self, request):
            queryset = ProductService.get_product()
            serializer = ProductSerializer(queryset, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class ProductsExportView(APIView):
    @cache_page(6)
    def get(self, request):
        products = Product.objects.select_related('category_id').prefetch_related('tags')
        wb = Workbook()
        ws = wb.active
        ws.title = "Products"
        ws.append(["ID", "Category", "Tags", "Name", "Description", "Price", "Created At"])
        for product in products:
            tags = ', '.join(tag.name for tag in product.tags.all())
            created_at = product.created_at.strftime('%Y-%m-%d %H:%M:%S')

            ws.append([product.id, product.category_id.name, tags,
                       product.name, product.description, product.price, created_at])
        response = HttpResponse(content_type="application/ms-excel")
        response["Content-Disposition"] = "attachment; filename=products.xlsx"
        wb.save(response)

        return response
