from django.contrib import admin
from Intense.models import User,Profile,user_balance,user_relation

# Register your models here.
admin.site.register(User)
admin.site.register(Profile)
admin.site.register(user_balance)
admin.site.register(user_relation)
