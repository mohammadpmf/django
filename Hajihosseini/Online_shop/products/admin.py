from django.contrib import admin

from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['title', 'description', 'price', 'active']
    list_display_links = ['title', 'description', 'price']
    list_editable = ['active']