from rest_framework import serializers
from catalog.models import Category, Producer, Discount, Promocode, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description',) # ('__all__')


class ProducerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producer
        fields = ('id', 'name', 'description', 'country',)


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = ('id', 'name', 'percent', 'date_start', 'date_end',)


class PromocodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promocode
        fields = ('id', 'name', 'percent', 'date_start', 'date_end', 'is_cumulative')


class ProductSerializer(serializers.ModelSerializer):
    discount = DiscountSerializer()
    category = CategorySerializer()
    producer = ProducerSerializer()

    class Meta:
        model = Product
        fields = ('id', 'name', 'price', 'count_on_stock', 'article', 'description',
                  'discount', 'category', 'producer')