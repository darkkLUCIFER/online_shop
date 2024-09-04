from django.contrib import admin

from apps.products.models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name','is_sub', 'active',)
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('parent_category',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'available')
    prepopulated_fields = {'slug': ('name',)}
    raw_id_fields = ('category',)
