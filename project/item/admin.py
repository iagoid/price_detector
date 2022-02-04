from item.models import Item
from django.contrib import admin
from sorl.thumbnail import get_thumbnail
from django.utils.html import format_html

# Permite a migração de dados
class ItemAdmin(admin.ModelAdmin):
    fields = ('link', )
    list_display = ['image_preview', 'name', 'updated_at' ]
    search_fields = ['name']
    readonly_fields = ('image_preview',)
    ordering = ('name',)

    def image_preview(self, obj):
        return obj.image_preview

    image_preview.short_description = 'Image Preview'
    image_preview.allow_tags = True

admin.site.register(Item, ItemAdmin)