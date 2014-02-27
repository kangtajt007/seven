from django.contrib import admin
from models import *

# Register your models here.


class CityInfoAdmin(admin.ModelAdmin):
    list_display = ( 'provinceName','townName','areaName','cityCode',)
    search_fields = ('provinceName', 'townName','areaName','cityCode',)

admin.site.register(CityInfo,CityInfoAdmin)