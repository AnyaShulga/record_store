from django.contrib import admin

from .models import Record, RecordGenre, RecordLabel, Order


@admin.register(RecordLabel)
class RecordLabelAdmin(admin.ModelAdmin):
    list_display = "pk", "name"
    list_display_links = "pk", "name"


@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = "pk", "artist", "album", "year", "condition", "price", "quantity"
    list_display_links = "pk", "artist", "album"
    ordering = "artist", "album"


@admin.register(RecordGenre)
class LpGenreAdmin(admin.ModelAdmin):
    list_display = "pk", "genre"
    list_display_links = "pk", "genre"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    pass
