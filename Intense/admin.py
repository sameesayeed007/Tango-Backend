from django.contrib import admin
from Intense.models import User,Profile,user_balance,user_relation,FAQ,Guest_user,Advertisement,ProductImpression,ProductImage,discount_product,Comment,CommentReply,Reviews,Category,Sub_Category,Sub_Sub_Category,ProductCode,Cupons,GroupProduct,Guest_user,Warehouse,Shop

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
admin.site.register(Comment)
admin.site.register(CommentReply)
admin.site.register(Reviews)
admin.site.register(Category)
admin.site.register(Sub_Category)
admin.site.register(Sub_Sub_Category)
admin.site.register(ProductCode)
admin.site.register(Cupons)
admin.site.register(GroupProduct)
admin.site.register(Warehouse)
admin.site.register(Shop)



