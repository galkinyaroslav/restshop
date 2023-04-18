from django.db.transaction import atomic
from rest_framework import serializers
from catalog.models import Category, Producer, Discount, Promocode, Product, OrderProducts, Order, Cashback
from datetime import date


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'description',)  # ('__all__')


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


class ProductInBasketSerializer(serializers.Serializer):
    name = serializers.CharField()
    price = serializers.DecimalField(max_digits=15, decimal_places=2)
    number_of_items = serializers.IntegerField()
    # discount = DiscountSerializer()


class BasketSerializer(serializers.Serializer):
    products = ProductInBasketSerializer(many=True)
    result_price = serializers.SerializerMethodField()

    def get_result_price(self, data):
        result_price = 0
        for item in data.get('products'):
            if item.get('discount'):
                percent = item.get('discount_percent')
                date_end = item.get('discount_date_end')
                delta = date.today() - date_end
                if delta.days <= 0:
                    result_price += (item.get('price') * (100 - percent) / 100) * item.get('number_of_items')
                else:
                    result_price += item.get('price') * item.get('number_of_items')
            else:
                result_price += item.get('price') * item.get('number_of_items')

        return result_price


class AddProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    number_of_items = serializers.IntegerField()


class DeleteProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProducts
        fields = ('product', 'count')


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, write_only=True)
    use_cashback = serializers.BooleanField(write_only=True)
    class Meta:
        model = Order
        fields = ('date_created', 'promocode','delivery_time',
                  'delivery_notif_in_time', 'delivery_method',
                  'delivery_address', 'delivery_status',
                  'payment_method', 'payment_status',
                  'user', 'result_price', 'products', 'use_cashback',)
        read_only_fields = ['date_created', 'delivery_status',
                            'payment_status', 'result_price']

    @atomic
    def create(self, validated_data):
        products = validated_data.pop('products')
        use_cashback = validated_data.pop('use_cashback')
        cashback = Cashback.objects.all().first()
        promocode= validated_data.get('promocode')
        # result_price = sum([record['product'].price*record['count'] for record in products])
        if promocode:
            delta_promocode = date.today() - promocode.date_end
            if delta_promocode.days > 0:
                promocode.percent = 0

        result_price = 0
        for record in products:
            if record['product'].discount:
                percent = record['product'].discount.percent
                date_end = record['product'].discount.date_end
                delta = date.today() - date_end
                if delta.days <= 0:
                    result_price += (record['product'].price * (100 - percent) / 100) * record['count']
                else:
                    result_price += record['product'].price * record['count']
            else:
                result_price += record['product'].price * record['count']

        if promocode.is_cumulative:
            result_price = result_price*(100-promocode.percent)/100

        if use_cashback:
            if self.context['request'].user.cashback_points <= result_price/2:
                if self.context['request'].user.cashback_points > cashback.threshold:
                    result_price -= self.context['request'].user.cashback_points
                    self.context['request'].user.cashback_points = 0
                    self.context['request'].user.save()
            else:
                if self.context['request'].user.cashback_points > cashback.threshold:
                    self.context['request'].user.cashback_points -= result_price/2
                    result_price -= result_price/2
                    self.context['request'].user.save()

        order = Order.objects.create(result_price=result_price,
                                     user=self.context['request'].user,
                                     **validated_data)
        for product in products:
            OrderProducts.objects.create(order=order, **product)
        return order
