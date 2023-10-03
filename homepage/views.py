from django.shortcuts import render
from .models import *

# Create your views here.
def main(request):
    categories = Category.objects.all().prefetch_related("topics")
    articles = Article.objects.all()
    return render(request, "main.html", {"categories": categories, "articles": articles})

def article(request, article_id, category, topic):
    categories = Category.objects.all().prefetch_related("topics")
    article = Article.objects.get(id=article_id)
    title = article.category.name + " - " + article.topic.name + " - " + article.title
    return render(request, "article.html", {"categories": categories, "article": article, "title": title})

def topic(request, category, topic_name):
    categories = Category.objects.all().prefetch_related("topics")
    topic = Topic.objects.get(name__iexact=topic_name)
    articles = Article.objects.filter(topic=topic)
    category = Category.objects.get(name__iexact=category)
    return render(request, "topic.html", {"categories": categories, "articles": articles, "topic": topic, "category": category})

def category(request, category):
    categories = Category.objects.all().prefetch_related("topics")
    cat = Category.objects.get(name__iexact=category)
    articles = Article.objects.filter(category=cat)
    topics = cat.topics.all()
    return render(request, "category.html", {"categories": categories, "articles": articles, "topics": topics, "category": cat})