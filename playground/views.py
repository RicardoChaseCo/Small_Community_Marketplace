from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.functions import Concat
from django.db.models import Q, F, Value, Func, Count
from django.db.models.aggregates import Count, Max, Min, Avg, Sum
from store.models import Product, Customer, Order, OrderItem, Collection
from django.contrib.contenttypes.models import ContentType
from tags.models import TaggedItem
from django.db import transaction, connection


def say_hello(request):
    result = Product.objects.aggregate(count=Count('id'))
    queryset1 = Customer.objects.annotate(full_name=Func(
        F('first_name'), Value(' '), F('last_name'), function='CONCAT'))

    collection = Collection.objects.get(pk=11)
    collection.title = 'Games'
    collection.featured_product = None
    collection.save()

    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        item.quantity = 1
        item.unit_price = 10
        item.save()

    queryset = Product.objects.raw('SELECT id, title FROM store_product')

    # Raw SQL Queries
    with connection.cursor() as cursor:
        cursor.execute('')

    return render(request, 'hello.html', {'result': list(queryset)})
