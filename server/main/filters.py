import django_filters
from .models import *
from django.db.models import Q


class ProductFilter(django_filters.FilterSet):
    query = django_filters.CharFilter(method="filter_by_name")
    category = django_filters.CharFilter(method="filter_by_category")

    class Meta:
        model = ProductModel
        fields = ['query', 'category']

    def filter_by_name(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value))
    
    def filter_by_category(self, queryset, name, value):
        return queryset.filter(Q(category__exact=value))
    
class ReviewFIlter(django_filters.FilterSet):
    product = django_filters.CharFilter(method="filter_by_product")

    class Meta:
        model = ProductReviewModel
        fields = ['product']

    def filter_by_product(self, queryset, name, value):
        return queryset.filter(Q(product__id__exact=value))