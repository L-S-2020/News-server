from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib import messages

# Create your views here.

# Startseite
def main(request):
    categories = Category.objects.all()
    articles = Article.objects.filter(sichtbar=True).order_by("-date")[:20]
    return render(request, "main.html", {"categories": categories, "articles": articles})

# Artikelseite mit Bewertung
def article(request, article_id, category,):
    # überprüfe, ob Get oder Post Anfrage
    if request.method == "POST":
        form = BewertungForm(request.POST)
        if form.is_valid():
            # nehme Variabeln aus dem Formular
            rating = form.cleaned_data["rating"]
            guess = form.cleaned_data["identifiziert"]
            article = Article.objects.get(id=article_id)
            art = article.art
            # überprüfe, ob die Schätzung richtig war und gib eine Nachricht aus
            if guess == 'ai' and art == 'gpt' or guess == 'ai' and art == 'mistral' or guess == 'mensch' and art == 'mensch':
                richtig = True
                messages.success(request, "Richtig!" )
            else:
                richtig = False
                messages.error(request, "Falsch!" )
            # speichere Bewertung in der Datenbank
            if request.user.is_authenticated:
                Bewertung.objects.create(article=article, rating=rating, user=request.user, art=art, identifiziert=guess, richtig=richtig)
            else:
                Bewertung.objects.create(article=article, rating=rating, user=None, art=art, identifiziert=guess, richtig=richtig)
            messages.success(request, "Bewertung erfolgreich abgegeben!" )
            article.bewertungen += 1
            article.save()
            return redirect('/neuerArtikel/' + str(article.id))
        else:
            messages.error(request, "Bewertung konnte nicht abgegeben werden!" )
    # nehme Variabeln aus der Datenbank
    categories = Category.objects.all()
    # suche Artikel in der Datenbank
    article = Article.objects.get(id=article_id)
    title = article.category.name + " - " + article.title
    form = BewertungForm()
    # Render die Seite mit den Variabeln
    return render(request, "article.html", {"categories": categories, "article": article, "title": title, "form": form})

# Katgorienseite
def category(request, category):
    categories = Category.objects.all()
    # suche Kategorie in der Datenbank
    cat = Category.objects.get(name__iexact=category)
    # suche zugehörige Artikel in der Datenbank
    articles = Article.objects.filter(category=cat, sichtbar=True)
    # Render die Seite mit den Variabeln
    return render(request, "category.html", {"categories": categories, "articles": articles, "category": cat})

# Konto Einstellungen
def settings(request):
    # überprüfe, ob der Benutzer eingeloggt ist
    if request.user.is_authenticated:
        return render(request, "settings.html")
    else:
        return redirect("/accounts/login")

# Impressum und Datenschutz
def impressum(request):
    return render(request, "impressum.html")

def datenschutz(request):
    return render(request, "datenschutz.html")

# Dashboard
def dashboard(request):
    return render(request, "dashboard.html")

def newArticle(request, alt_id):
    # Hole Artikel mit wenigsten Bewertungen
    if alt_id == 000:
        articles = Article.objects.filter(sichtbar=True).order_by("bewertungen")[:2]
    else:
        articles = Article.objects.filter(sichtbar=True).exclude(id=alt_id).order_by("bewertungen")[:2]
    article = articles[0]
    # Weiterleitung zum Artikel
    return redirect(article.url())

def welcome(request):
    return render(request, "welcome.html")

# Api zum Hochladen von Artikeln
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# überprüfe, ob der Artikel schon existiert
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

# speichere den Artikel in der Datenbank
@csrf_exempt
def uploadArticle(request):
    if request.method == "POST":
        if request.POST.get("key") == "123":
            # nehme Variabeln aus dem Formular
            title = request.POST.get("title")
            description = request.POST.get("description")
            content = request.POST.get("content")
            source = request.POST.get("source")
            image = request.FILES['image']
            article_id = request.POST.get("article_id")
            kat = Category.objects.get(id=request.POST.get("kategorie"))
            art = request.POST.get("art")
            # speichere den Artikel in der Datenbank
            Article.objects.create(title=title, description=description, content=content, source=source, article_id=article_id, category=kat, image=image, sichtbar=False, art=art)
            # speichere die Tags in der Datenbank
            tags = str(request.POST.get("tags"))
            tags = tags.split(",")
            for t in tags:
                if not Tag.objects.filter(name=t).exists():
                    Tag.objects.create(name=t)
                tag = Tag.objects.get(name=t)
                article = Article.objects.get(article_id=article_id)
                article.tags.add(tag)
            # gebe eine Erfolgsmeldung zurück
            return JsonResponse({"success": True})
        else:
            return JsonResponse({"success": False})
    else:
        return JsonResponse({"success": False})

# Dashboard
# definiere Cache Variabeln
cache_anzahl = 0
cache = {"anzahl": 0, "durchschnitt": 0, "durchschnitt_gpt": 0, "durchschnitt_mistral": 0, "durchschnitt_mensch": 0, "richtig": 0, "falsch": 0}

# Dashboard View/Api
def aktualisieren(request):
    global cache_anzahl
    global cache
    bewertungen = Bewertung.objects.all()
    anzahl = len(bewertungen)
    # überprüfe, ob sich die Anzahl der Bewertungen, seit dem letzten Cachen, geändert hat
    if anzahl != cache_anzahl:
        durchschnitt = 0
        # berechne den Durchschnitt der Bewertungen
        if anzahl != 0:
            for b in bewertungen:
                durchschnitt += b.rating
            durchschnitt = durchschnitt / anzahl
        # berechne den Durchschnitt der Bewertungen für die verschiedenen KI's
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
        # hole die Anzahl der richtigen und falschen Schätzungen
        richtig = Bewertung.objects.filter(richtig=True)
        richtig_anzahl = len(richtig)
        falsch_anzahl = anzahl - richtig_anzahl
        # aktualisiere den Cache
        cache = {"anzahl": anzahl, "durchschnitt": durchschnitt, "durchschnitt_gpt": durchschnitt_gpt, "durchschnitt_mistral": durchschnitt_mistral, "durchschnitt_mensch": durchschnitt_mensch, "richtig": richtig_anzahl, "falsch": falsch_anzahl}
    # gebe den Cache zurück
    return JsonResponse(cache)


