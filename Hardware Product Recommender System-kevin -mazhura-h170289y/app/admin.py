from django.contrib import admin
from . models import *
# Register your models here.
admin.site.site_header = "Hardware Stores"
admin.site.index_title = "Welcome to Hardware Store"
admin.site.site_title = "Hardware store admin"

admin.site.register(Person)
admin.site.register(Customer)
admin.site.register(Seller)
admin.site.register(OnlineStore)
admin.site.register(StoreCategory)
# admin.site.register()


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
   list_display = ("name", "store","product_category")
   list_filter = ("name", "store","product_category")
   search_fields = ("name__startswith", )
    
