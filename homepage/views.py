from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.
def main(request):
    categories = Category.objects.all()
    articles = Article.objects.filter(sichtbar=True).order_by("-date")[:20]
    return render(request, "main.html", {"categories": categories, "articles": articles})

def article(request, article_id, category,):
    if request.method == "POST":
        form = BewertungForm(request.POST)
        if form.is_valid():
            rating = form.cleaned_data["rating"]
            guess = form.cleaned_data["identifiziert"]
            article = Article.objects.get(id=article_id)
            art = article.art
            if guess == 'ai' and art == 'gpt' or guess == 'ai' and art == 'mistral' or guess == 'mensch' and art == 'mensch':
                richtig = True
                messages.success(request, "Richtig!" )
            else:
                richtig = False
                messages.error(request, "Falsch!" )
            if request.user.is_authenticated:
                Bewertung.objects.create(article=article, rating=rating, user=request.user, art=art, identifiziert=guess, richtig=richtig)
            else:
                Bewertung.objects.create(article=article, rating=rating, user=None, art=art, identifiziert=guess, richtig=richtig)
            messages.success(request, "Bewertung erfolgreich abgegeben!" )
        else:
            messages.error(request, "Bewertung konnte nicht abgegeben werden!" )
    categories = Category.objects.all()
    article = Article.objects.get(id=article_id)
    title = article.category.name + " - " + article.title
    form = BewertungForm()
    return render(request, "article.html", {"categories": categories, "article": article, "title": title, "form": form})


def category(request, category):
    categories = Category.objects.all()
    cat = Category.objects.get(name__iexact=category)
    articles = Article.objects.filter(category=cat, sichtbar=True)
    return render(request, "category.html", {"categories": categories, "articles": articles, "category": cat})


def settings(request):
    if request.user.is_authenticated:
        return render(request, "settings.html")
    else:
        return redirect("/accounts/login")

def impressum(request):
    return render(request, "impressum.html")

def datenschutz(request):
    return render(request, "datenschutz.html")

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
            image = request.FILES['image']
            article_id = request.POST.get("article_id")
            kat = Category.objects.get(id=request.POST.get("kategorie"))
            art = request.POST.get("art")
            Article.objects.create(title=title, description=description, content=content, source=source, article_id=article_id, category=kat, image=image, sichtbar=False, art=art)
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

# Dashboard
cache_anzahl = 0
cache = {"anzahl": 0, "durchschnitt": 0, "durchschnitt_gpt": 0, "durchschnitt_mistral": 0, "durchschnitt_mensch": 0, "richtig": 0, "falsch": 0}
def aktualisieren(request):
    global cache_anzahl
    global cache
    bewertungen = Bewertung.objects.all()
    anzahl = len(bewertungen)
    if anzahl != cache_anzahl:
        durchschnitt = 0
        if anzahl != 0:
            for b in bewertungen:
                durchschnitt += b.rating
            durchschnitt = durchschnitt / anzahl
        gpt_bewertungen = Bewertung.objects.filter(art="gpt")
        anzahl_gpt = len(gpt_bewertungen)
        durchschnitt_gpt = 0
        if anzahl_gpt != 0:
            for b in gpt_bewertungen:
                durchschnitt_gpt += b.rating
            durchschnitt_gpt = durchschnitt_gpt / anzahl_gpt
        mistral_bewertungen = Bewertung.objects.filter(art="mistral")
        anzahl_mistral = len(mistral_bewertungen)
        durchschnitt_mistral = 0
        if anzahl_mistral != 0:
            for b in mistral_bewertungen:
                durchschnitt_mistral += b.rating
            durchschnitt_mistral = durchschnitt_mistral / anzahl_mistral
        mensch_bewertungen = Bewertung.objects.filter(art="mensch")
        anzahl_mensch = len(mensch_bewertungen)
        durchschnitt_mensch = 0
        if anzahl_mensch != 0:
            for b in mensch_bewertungen:
                durchschnitt_mensch += b.rating
            durchschnitt_mensch = durchschnitt_mensch / anzahl_mensch
        richtig = Bewertung.objects.filter(richtig=True)
        richtig_anzahl = len(richtig)
        falsch_anzahl = anzahl - richtig_anzahl
        cache = {"anzahl": anzahl, "durchschnitt": durchschnitt, "durchschnitt_gpt": durchschnitt_gpt, "durchschnitt_mistral": durchschnitt_mistral, "durchschnitt_mensch": durchschnitt_mensch, "richtig": richtig_anzahl, "falsch": falsch_anzahl}
    return JsonResponse(cache)

def dashboard(request):
    return render(request, "dashboard.html")

