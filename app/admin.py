from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
class UserSort(ImportExportModelAdmin):
    pass
admin.site.register(Hospital,UserSort)
admin.site.register(WelcomeNotes)
admin.site.register(Bank)
admin.site.register(Assylum)
admin.site.register(ContactUs)
admin.site.register(Gp)
admin.site.register(Refuse)
admin.site.register(Query)
admin.site.register(Querystatus)
admin.site.register(Messages_Assigned)