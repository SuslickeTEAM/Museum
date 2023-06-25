from django.contrib import admin
from .models import *

class ExhibitAdmin(admin.ModelAdmin):
    list_display = ('title', 'description',)
    list_filter = ('title',)


admin.site.register(Exhibit, ExhibitAdmin)
admin.site.register(Event)
admin.site.register(Category)