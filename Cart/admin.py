from django.contrib import admin
from Intense.models import Product , Order , OrderDetails, ProductPrice , Userz ,BillingAddress, ProductPoint,ProductSpecification

# Register your models here.
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(ProductPrice)
admin.site.register(Userz)
admin.site.register(BillingAddress)
admin.site.register(ProductPoint)
admin.site.register(ProductSpecification)