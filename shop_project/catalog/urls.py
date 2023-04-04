from django.urls import path, include
from catalog.views import  ProducersListView, DiscountsListView, \
    PromocodesListView, ProductsListView, ProducerProductsView, CategoriesListView,  CategoryProductsView

urlpatterns = [
    # path('categories/', CategoryView.as_view(), name='categories'),
    # path('categories/<int:category_id>/', CategoryView.as_view(), name='category-products'),
    path('categories/', CategoriesListView.as_view(), name='categories'),
    path('categories/<int:category_id>/', CategoryProductsView.as_view(), name='category-products'),

    path('producers/', ProducersListView.as_view(), name='producers'),
    path('producers/<int:producer_id>/', ProducerProductsView.as_view(), name='producer-products'),

    path('discounts/', DiscountsListView.as_view()),
    path('promocodes/', PromocodesListView.as_view()),
    path('products/', ProductsListView.as_view()),

]
