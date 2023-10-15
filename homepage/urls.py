from django.urls import path
from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("article/<str:category>/<str:topic>/<int:article_id>", views.article, name="article"),
    path("article/<str:category>/<str:topic_name>/", views.topic, name="topic"),
    path("article/<str:category>/", views.category, name="category"),
    path("api/checkNumber", views.checkNumber, name="checkNumber"),
    path("api/uploadArticle", views.uploadArticle, name="uploadArticle"),
]
