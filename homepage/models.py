from django.db import models

# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    content = models.TextField()
    source = models.ForeignKey('source', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to="media/", null=True, blank=True)
    tags = models.ManyToManyField('tag', blank=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=True, blank=True)
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    def url(self):
        url = "/article/" + self.category.name + "/" + self.topic.name + "/" + str(self.id)
        return url

class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    articles = models.ManyToManyField(Article)

    def __str__(self):
        return self.name

class Source(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100)
    topics = models.ManyToManyField('Topic', blank=True, related_name="categories")
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def url(self):
        url = "/article/" + self.name
        return url
class Topic(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name

    def url(self):
        url = "/article/" + Category.objects.get(topics=self).name + "/" + self.name
        return url