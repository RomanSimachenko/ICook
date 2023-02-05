from django.contrib import admin
from . import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'thumbnail', 'description')
    list_display_links = ('slug', 'name',)
    exclude = ('slug',)


@admin.register(models.Area)
class AreaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('name',)


@admin.register(models.Measure)
class MeasureAdmin(admin.ModelAdmin):
    list_display = ('amount', 'unit',)
    list_display_links = ('unit',)


@admin.register(models.Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)
    list_display_links = ('name',)


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'thumbnail', 'description')
    list_display_links = ('slug', 'name',)
    exclude = ('slug',)


@admin.register(models.Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ('slug', 'name', 'category', 'area', 'thumbnail', 'get_tags', 'cooking_difficulty', 'date_created',)
    list_display_links = ('slug', 'name',)
    exclude = ('slug',)
