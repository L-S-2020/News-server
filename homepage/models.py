from django.db import models

# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    content = models.TextField()
    source = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="media/", null=True, blank=True, default="media/default.jpg")
    tags = models.ManyToManyField('Tag', blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    article_id = models.CharField(max_length=500, null=True, blank=True)
    sichtbar = models.BooleanField(default=False)
    art = models.CharField(max_length=20, null=True, blank=True)

    def __str__(self):
        return self.title

    def url(self):
        url = "/article/" + self.category.name + "/" + str(self.id)
        return url

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Category(models.Model):
    id = models.CharField(max_length=15, primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def url(self):
        url = "/article/" + self.name
        return url

class Bewertung(models.Model):
    id = models.AutoField(primary_key=True)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True, blank=True)
    rating = models.FloatField()
    art = models.CharField(max_length=100, null=True, blank=True)
    identifiziert = models.CharField(max_length=100, null=True, blank=True)
    richtig = models.BooleanField(default=False)

    def article_kat(self):
        return self.article.article_id
