from django.contrib import admin
from mptt.admin import DraggableMPTTAdmin
# Register your models here.
from django.contrib.admin.widgets import FilteredSelectMultiple

from Intense.models import Product, Variation, Category, GroupProduct , ProductImage,ProductViews

admin.site.register(ProductImage)


# admin.site.register(Variation)

# #admin.site.register(ProductImage)
# admin.site.register(Product)
# admin.site.register(ProductViews)

# admin.site.register(Category)
# admin.site.register(GroupProduct)
