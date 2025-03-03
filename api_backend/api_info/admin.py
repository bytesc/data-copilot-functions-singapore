from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import ApiGroup, ApiInfo


# Register your models here.
class ApiGroupAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in ApiGroup._meta.fields]
    list_filter = [field.name for field in ApiGroup._meta.fields]
    search_fields = [field.name for field in ApiGroup._meta.fields]


class ApiInfoAdmin(ImportExportModelAdmin):
    list_display = [field.name for field in ApiInfo._meta.fields]
    list_filter = [field.name for field in ApiInfo._meta.fields]
    search_fields = [field.name for field in ApiInfo._meta.fields]
    autocomplete_fields = ['api_group']


admin.site.register(ApiInfo, ApiInfoAdmin)
admin.site.register(ApiGroup, ApiGroupAdmin)
