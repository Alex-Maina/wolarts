from django.contrib import admin
from . import models



'''
#modify the collection page
@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    search_fields=['title']
    

#modify the products-admin page
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['name']
    }
    autocomplete_fields =['collection']
    list_display = ['name', 'price','inventory_status', 'collection']
    list_editable = ['price', 'collection']
    ordering =['name']
    search_fields = ['title__istartswith']
    list_filter = ['collection']

    @admin.display(ordering='inventory')
    def inventory_status(self,product):
        if product.inventory < 10:
            return 'LOW'
        return 'OK'


#modify the customer page
@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
'''


admin.site.register(models.Collection)
admin.site.register(models.Product)
admin.site.register(models.Customer)
admin.site.register(models.Order)
admin.site.register(models.OrderItem)
admin.site.register(models.ShippingAddress)

