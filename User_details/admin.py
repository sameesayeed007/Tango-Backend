from django.contrib import admin

# Register your models here.
from Intense.models import Profile, Address, User , UserManager , DeactivateUser, GuestUser , user_relation

admin.site.register(Profile)
admin.site.register(User)
admin.site.register(DeactivateUser)
admin.site.register(user_relation)
admin.site.register(Address)
admin.site.register(GuestUser)

#admin.site.register(DeactivateUser)
