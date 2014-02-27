from django.contrib import admin
from forum.models import *

class BlogAdmin(admin.ModelAdmin):
    list_display = ( 'subject','author','type_id',)
    search_fields = ('author', 'subject','tag',)
    date_hierarchy = 'create_time'
    ordering = ('-create_time',)
    #filter_horizontal = ('author',)
    raw_id_fields = ('author',)

admin.site.register(BlogType)
admin.site.register(Blog,BlogAdmin)
admin.site.register(BlogComment)
