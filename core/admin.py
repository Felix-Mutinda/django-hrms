from django.contrib import admin

from core.models import User, Employer, Employee, Asset, AssignedAsset

admin.site.register(User)
admin.site.register(Employer)
admin.site.register(Employee)
admin.site.register(Asset)
admin.site.register(AssignedAsset)