from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price','new', 'discount', 'stock', 'created', 'updated', 'is_available']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_available', 'category', 'new']
    list_editable = ['price','discount', 'is_available', 'stock', 'new']
    readonly_fields = ['created', 'updated', ]
    # inlines = [ProductGalleryInline]