from django.contrib import admin
from Intense.models import User,Profile,user_balance,user_relation,FAQ,Guest_user,Advertisement,ProductImpression,ProductImage,discount_product

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(user_balance)
admin.site.register(user_relation)
admin.site.register(FAQ)
admin.site.register(Guest_user)
admin.site.register(ProductImage)
admin.site.register(discount_product)
admin.site.register(ProductImpression)

