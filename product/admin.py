from django.contrib import admin
from .models import Product, ProductCategory

class ProductAdminPanel(admin.ModelAdmin):
    # readonly_fields = ('title', 'price', 'description', 'image', 'categories', 'author')
    list_display = ('id','title', 'price', 'image',  'author', 'date_created', 'date_updated')

class ProductCategoryAdminPanel(admin.ModelAdmin):
    # readonly_fields = ('title', 'description')
    list_display = ('id','title', )
    
admin.site.register(Product, ProductAdminPanel)
admin.site.register(ProductCategory, ProductCategoryAdminPanel)