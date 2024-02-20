from django.db import models

# Datenbank Modelle

# Artikelmodell
class Article(models.Model):
    # einmalige ID (numerisch) (wird automatisch generiert)
    id = models.AutoField(primary_key=True)
    # Titel des Artikels
    title = models.CharField(max_length=100)
    # Beschreibung des Artikels
    description = models.TextField(null=True, blank=True)
    # Inhalt des Artikels
    content = models.TextField()
    # Quelle des Artikels
    source = models.CharField(max_length=100, null=True, blank=True)
    # Erstellungsdatum des Artikels
    date = models.DateTimeField(auto_now_add=True)
    # Bild des Artikels
    image = models.ImageField(upload_to="media/", null=True, blank=True, default="media/default.jpg")
    # Schlagwörter des Artikels
    tags = models.ManyToManyField('Tag', blank=True)
    # Kategorie des Artikels
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    # Eindeutige ID des Artikels (alpanumerisch)
    article_id = models.CharField(max_length=500, null=True, blank=True)
    # Sichtbarkeit des Artikels
    sichtbar = models.BooleanField(default=False)
    # Art des Artikels (z.B. GPT-3.5 oder Mistral)
    art = models.CharField(max_length=20, null=True, blank=True)

    # Gebe den Titel des Artikels zurück
    def __str__(self):
        return self.title

    # Erstelle die URL des Artikels
    def url(self):
        url = "/article/" + self.category.name + "/" + str(self.id)
        return url

# Tagmodell
class Tag(models.Model):
    # einmalige ID (numerisch) (wird automatisch generiert)
    id = models.AutoField(primary_key=True)
    # Name des Schlagworts
    name = models.CharField(max_length=100)

    # Gebe den Namen des Schlagworts zurück
    def __str__(self):
        return self.name

# Kategoriemodell
class Category(models.Model):
    # interner Name der Kategorie (für das Klassifizierungsmodell)
    id = models.CharField(max_length=15, primary_key=True)
    # Name der Kategorie
    name = models.CharField(max_length=100)
    # Beschreibung der Kategorie
    description = models.TextField(null=True, blank=True)

    # Gebe den Namen der Kategorie zurück
    def __str__(self):
        return self.name

    # Erstelle die URL der Kategorie
    def url(self):
        url = "/article/" + self.name
        return url

# Bewertungsmodell
class Bewertung(models.Model):
    # einmalige ID (numerisch) (wird automatisch generiert)
    id = models.AutoField(primary_key=True)
    # Artikel, der bewertet wurde
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    # Benutzer, der den Artikel bewertet hat
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    # Bewertung des Artikels
    rating = models.FloatField()
    # Art des Artikels (z.B. GPT-3.5 oder Mistral)
    art = models.CharField(max_length=100, null=True, blank=True)
    # Schätzung des Nutzers
    identifiziert = models.CharField(max_length=100, null=True, blank=True)
    # Wurde die Quelle richtig identifiziert?
    richtig = models.BooleanField(default=False)

    # Gebe die ID des zugehörigen Artikels zurück
    def article_kat(self):
        return self.article.article_id
