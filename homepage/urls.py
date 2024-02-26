from django.urls import path
from . import views

# Definiere die URL Muster
urlpatterns = [
    # Startseite
    path("", views.main, name="main"),
    # Artikelseite
    path("article/<str:category>/<int:article_id>", views.article, name="article"),
    # Kategorienseite
    path("article/<str:category>/", views.category, name="category"),
    # API
    path("api/checkNumber", views.checkNumber, name="checkNumber"),
    path("api/uploadArticle", views.uploadArticle, name="uploadArticle"),
    path("api/aktualisieren", views.aktualisieren, name="aktualisieren"),
    # Konto Einstellungen
    path("settings/", views.settings, name="settings"),
    # Impressum und Datenschutz
    path("impressum/", views.impressum, name="impressum"),
    path("datenschutz/", views.datenschutz, name="datenschutz"),
    # Dashboard
    path("dashboard/", views.dashboard, name="dashboard"),
    # Neuer Artikel
    path("neuerArtikel/<int:alt_id>", views.newArticle, name="newArticle"),
]
