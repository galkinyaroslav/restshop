from django.contrib import admin
from catalog.models import Category, Producer, Discount, Promocode, Product
# Register your models here.

admin.site.register(Category)
admin.site.register(Producer)
admin.site.register(Discount)
admin.site.register(Promocode)
admin.site.register(Product)

