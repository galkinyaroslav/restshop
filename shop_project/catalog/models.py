from django.db import models
from users.models import CustomUser


# Create your models here.


class Cashback(models.Model):
    percent = models.IntegerField()
    threshold = models.IntegerField()


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Producer(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Discount(models.Model):
    percent = models.IntegerField()
    name = models.CharField(max_length=100)
    date_start = models.DateField()
    date_end = models.DateField()

    def __str__(self):
        return f'{self.name} {self.percent}%'


class Product(models.Model):
    name = models.CharField(max_length=256)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    count_on_stock = models.IntegerField()
    article = models.CharField(max_length=50)
    description = models.TextField()
    discount = models.ForeignKey(Discount, null=True, blank=True, on_delete=models.SET_NULL)
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)
    producer = models.ForeignKey(Producer, null=True, blank=True, on_delete=models.SET_NULL)

    def __str__(self):
        return f'{self.name}'


class Promocode(models.Model):
    name = models.CharField(max_length=100)
    percent = models.IntegerField()
    date_start = models.DateField()
    date_end = models.DateField()
    is_cumulative = models.BooleanField()

    def __str__(self):
        return f'{self.name}'


class Basket(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(null=True, blank=True)


class Order(models.Model):
    DELIVERY_METHOD = (
        ('Courier', 'Courier'),
        ('Self-delivery', 'Self-delivery'),
        ('Post', 'Post'),
        ('Post box', 'Post box')
    )
    PAYMENT_METHOSDS = (
        ('Cash', 'Cash'),
        ('Card', 'Card'),
        ('Card online', 'Card online'),
    )

    PAYMENT_STATUS = (
        ('Paid', 'Paid'),
        ('In process', 'In process')
    )
    DELIVERY_STATUS = (
        ('Delivered', 'Delivered'),
        ('In process', 'In process')
    )
    DELIVERY_NOTIF_IN_TIME = (
        (24, 24),
        (6, 6),
        (1, 1),
    )
    date_created = models.DateTimeField(auto_now_add=True)
    promocode = models.ForeignKey(Promocode, null=True, blank=True, on_delete=models.SET_NULL)
    delivery_time = models.DateTimeField()
    dilivery_notif_in_time = models.IntegerField(choices=DELIVERY_NOTIF_IN_TIME, null=True, default=None)
    delivery_method = models.CharField(max_length=15, choices=DELIVERY_METHOD, default='Self-delivery')
    delivery_address = models.CharField(max_length=256)
    delivery_status = models.CharField(max_length=15, choices=DELIVERY_STATUS, default='In process')
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOSDS, default='Card')
    payment_status = models.CharField(max_length=15, choices=PAYMENT_STATUS, default='In process')
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.SET_NULL)
    result_price = models.DecimalField(max_digits=15, decimal_places=2)


class OrderProducts(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
