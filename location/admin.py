from django.contrib import admin

from location.models import Province, District, Municipality, Ward


class ProvinceAdmin(admin.ModelAdmin):
    list_display = ("name", "nepali_name", "number")


class DistrictAdmin(admin.ModelAdmin):
    list_display = ("name", "nepali_name", "province")
    list_filter = ("province",)
    search_fields = ("name", "nepali_name",)


class MunicipalityAdmin(admin.ModelAdmin):
    list_display = ("name", "nepali_name", "district", "is_approved", "approved_by", "approved_at")
    list_filter = ("district", "district__province")
    search_fields = ("name", "nepali_name",)


class WardAdmin(admin.ModelAdmin):
    list_display = ("name", "nepali_name", "number", "municipality")
    list_filter = ("municipality", "municipality__district", "municipality__district__province")
    search_fields = ("name", "nepali_name",)
    list_per_page = 15


admin.site.register(Province, ProvinceAdmin)
admin.site.register(District, DistrictAdmin)
admin.site.register(Municipality, MunicipalityAdmin)
admin.site.register(Ward, WardAdmin)
