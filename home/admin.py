from django.contrib import admin
from .models import Popular_Products, For_You



@admin.register(Popular_Products)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price','new', 'discount', 'stock', 'created', 'updated', 'is_available']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_available', 'category', 'new']
    list_editable = ['price','discount', 'is_available', 'stock', 'new']
    readonly_fields = ['created', 'updated', ]
    # inlines = [ProductGalleryInline]



@admin.register(For_You)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price','new', 'discount', 'stock', 'created', 'updated', 'is_available']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['is_available', 'category', 'new']
    list_editable = ['price','discount', 'is_available', 'stock', 'new']
    readonly_fields = ['created', 'updated', ]
    # inlines = [ProductGalleryInline]