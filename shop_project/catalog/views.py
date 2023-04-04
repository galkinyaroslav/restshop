from catalog.models import Category, Producer, Discount, Promocode, Product
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import generics
# from rest_framework.mixins import ListModelMixin

from catalog.serializers import CategorySerializer, ProducerSerializer, DiscountSerializer, \
    PromocodeSerializer, ProductSerializer


# Create your views here.


class CategoriesListView(ListAPIView):
    queryset = Category.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer


class CategoryProductsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, category_id):
        queryset = Product.objects.filter(category__id=category_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


# class CategoryView(generics.GenericAPIView, ListModelMixin):
#     permission_classes = (AllowAny,)
#     lookup_url_kwarg = 'category_id'
#
#     def get_serializer_class(self):
#         if 'category_id' in self.kwargs:
#             return ProductSerializer
#         else:
#             return CategorySerializer
#
#     def get_queryset(self):
#         if 'category_id' in self.kwargs:
#             category_id = self.kwargs['category_id']
#             return Product.objects.filter(category__id=category_id)
#         else:
#             return Category.objects.all()
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)


class ProducersListView(ListAPIView):
    queryset = Producer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProducerSerializer


class ProducerProductsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, producer_id):
        queryset = Product.objects.filter(producer__id=producer_id)
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class DiscountsListView(ListAPIView):
    queryset = Discount.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = DiscountSerializer


class PromocodesListView(ListAPIView):
    queryset = Promocode.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PromocodeSerializer


class ProductsListView(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = ProductSerializer
