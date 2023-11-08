from django.shortcuts import render
from .models import *

# Create your views here.
def main(request):
    categories = Category.objects.all().prefetch_related("topics")
    articles = Article.objects.all().order_by("-date")[:20]
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

# Api zum Hochladen von Artikeln
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

@csrf_exempt
def checkNumber(request):
    if request.method == "POST":
        id = request.POST.get("article_id")
        if Article.objects.filter(article_id=id).exists():
            return JsonResponse({"artikel": "existiert"})
        else:
            return JsonResponse({"artikel": "existiert_nicht"})
    else:
        return JsonResponse({"success": False})

@csrf_exempt
def uploadArticle(request):
    if request.method == "POST":
        if request.POST.get("key") == "123":
            title = request.POST.get("title")
            description = request.POST.get("description")
            content = request.POST.get("content")
            source = request.POST.get("source")
            url = request.POST.get("url")
            image = request.FILES['image']
            article_id = request.POST.get("article_id")
            kat = Category.objects.get(name="Politik")
            topic = Topic.objects.get(name="Inland")
            Article.objects.create(title=title, description=description, content=content, source=source, article_id=article_id, category=kat, topic=topic, image=image)
            tags = str(request.POST.get("tags"))
            tags = tags.split(",")
            for t in tags:
                if not Tag.objects.filter(name=t).exists():
                    Tag.objects.create(name=t)
                tag = Tag.objects.get(name=t)
                article = Article.objects.get(article_id=article_id)
                article.tags.add(tag)
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
    else:
        return JsonResponse({"success": False})