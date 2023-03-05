from django.contrib import admin, messages
from django.contrib.contenttypes.admin import GenericTabularInline
from . import models
from django.http.request import HttpRequest
from django.db.models import Count
from django.utils.html import format_html, urlencode
from django.urls import reverse

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    actions = ['clear_inventory']
    list_display = ['title', 'unit_price',
                    'inventory_status', 'collection_title']
    list_editable = ['unit_price']
    list_filter = ['collection', 'last_update']
    list_per_page = 10
    list_select_related = ['collection']

    def collection_title(self, product):
        return product.collection.title

    @admin.display(ordering='inventory')
    def inventory_status(self, product):
        if product.inventory < 10:
            return 'low'
        else:
            return 'OK'

    @admin.action(description='Clear Inventory')
    def clear_inventory(self, request, queryset):
        updated_count = queryset.update(inventory=0)
        self.message_user(
            request,
            f'{updated_count} products were updated!',
            messages.ERROR
        )


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'membership']
    list_editable = ['membership']
    ordering = ['first_name', 'last_name']
    list_per_page = 10
    search_fields = ['first_name__istartswith', 'last_name__istartswith']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'placed_at', 'customer']


class CollectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'products_count']

    @admin.display(ordering='products_count')
    def products_count(self, collection):
        url = reverse('admin:store_product_changelist') + '?' + urlencode({
            'collection__id': str(collection.id)
        })
        return format_html('<a href="{}">{}</a>', url, collection.products_count)

    def get_queryset(self, request):
        return super().get_queryset(request).annotate(
            products_count=Count('product')
        )


admin.site.register(models.Collection, CollectionAdmin)

admin.site.register(models.Product, ProductAdmin)

admin.site.register(models.Customer, CustomerAdmin)

admin.site.register(models.Order, OrderAdmin)
