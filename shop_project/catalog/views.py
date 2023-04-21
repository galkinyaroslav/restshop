from catalog.models import Category, Producer, Discount, Promocode, Product, Basket
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
# from rest_framework import generics
# from rest_framework.mixins import ListModelMixin
from django.db.models import F
from django.shortcuts import get_object_or_404
from catalog.tasks import some_task
from catalog.serializers import CategorySerializer, ProducerSerializer, DiscountSerializer, \
    PromocodeSerializer, ProductSerializer, BasketSerializer, AddProductSerializer, DeleteProductSerializer


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
        some_task.delay()

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


class DiscountProductsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, discount_id):

        if discount_id == 0:
            queryset = Product.objects.filter(discount=None)
        elif discount_id > 0:
            queryset = Product.objects.filter(discount__id=discount_id)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)


class PromocodesListView(ListAPIView):
    queryset = Promocode.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = PromocodeSerializer


class ProductsListView(ListAPIView):
    queryset = Product.objects.all()
    permission_classes = (AllowAny,)

    serializer_class = ProductSerializer




class BasketView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        # select_related prefetch_related --->>> for manyTomany, oneTomany relations
        user = request.user
        basket = Product.objects.prefetch_related('basket_set').filter(basket__user=user).values(
            'name', 'price', 'discount', number_of_items=F('basket__count'),
            discount_percent=F('discount__percent'), discount_date_end=F('discount__date_end'),
            discount_name=F('discount__name'), discount_date_start=F('discount__date_start')
        )
        serializer = BasketSerializer({'products': basket})
        return Response(serializer.data)

    def post(self,request):
        input_serializer = AddProductSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=input_serializer.data.get('product_id'))

        # basket = Basket(user=request.user,
        #                 product=product,
        #                 count=input_serializer.data.get('number_of_items'))
        # basket.save()
        basket_object, create = Basket.objects.get_or_create(user=request.user, product=product)
        if basket_object.count:
            basket_object.count += input_serializer.data.get('number_of_items')
        else:
            basket_object.count = input_serializer.data.get('number_of_items')

        if basket_object.count <=0:
            basket_object.delete()
        else:
            basket_object.save()

        return Response()

    def delete(self, request):
        input_serializer = DeleteProductSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        product = get_object_or_404(Product, id=input_serializer)

        Basket.objects.get(user=request.user, product=product).delete()
        return Response()
