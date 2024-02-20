from django.contrib import admin
from .models import *

# Aktionen für den Adminbereich

# Aktion: Markiere Artikel als unsichtbar
@admin.action(description='Markierte Artikel als unsichtbar markieren')
def make_unsichtbar(modeladmin, request, queryset):
    queryset.update(sichtbar=False)

# Aktion: Markiere Artikel als sichtbar
@admin.action(description='Markierte Artikel als sichtbar markieren')
def make_sichtbar(modeladmin, request, queryset):
    queryset.update(sichtbar=True)

# Füge die Modelle zum Adminbereich hinzu
admin.site.register(Category)
admin.site.register(Tag)

# zeige unter Bewertung den Artikel an
@admin.register(Bewertung)
class BewertungAdmin(admin.ModelAdmin):
    list_display = ("article_kat", "rating", "article",)
    list_filter = ("article",)
    search_fields = ("article",)

# mache Artikel nach Kategorie und Sichtbarkeit filterbar
@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("article_id", "sichtbar","title", "category", "date", )
    list_filter = ("category", "sichtbar",)
    search_fields = ("title", "category", "topic",)
    actions = [make_unsichtbar, make_sichtbar]