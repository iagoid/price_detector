from django.db import models
from django.utils.html import mark_safe
from django.utils.html import format_html
from sorl.thumbnail import get_thumbnail

class Item(models.Model):
    name = models.CharField('Nome', null=True, blank=True, max_length=300)
    link = models.CharField('Link', max_length=200)
    price = models.FloatField('Preço', null=True, blank=True)
    image = models.CharField('Imagem', null=True, blank=True, max_length=300)

    created_at = models.DateTimeField('Criado em', auto_now_add = True)
    updated_at = models.DateTimeField('Modificado em', auto_now = True)

    @property
    def image_preview(self):
        if self.image:
            return mark_safe('<img src="{}" width="75px" height="75px" />'.format(self.image))
        return ""

    def __str__(self):
        return self.name or self.link

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'
        ordering = ['created_at']
