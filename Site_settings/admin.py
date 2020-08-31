from django.contrib import admin
from Intense.models import RolesPermissions,CompanyInfo,Banner_Image,Banner,Currency,APIs,Settings,Theme

# Register your models here.
admin.site.register(RolesPermissions)
admin.site.register(CompanyInfo)
admin.site.register(Banner)
admin.site.register(Banner_Image)
admin.site.register(Currency)
admin.site.register(APIs)
admin.site.register(Settings)
admin.site.register(Theme)
