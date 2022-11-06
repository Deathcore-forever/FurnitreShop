from django.contrib import admin

from .models import Furniture


class FurAdmin(admin.ModelAdmin):
    list_display = ('id', 'name_fur', 'price')


admin.site.register(Furniture, FurAdmin)
