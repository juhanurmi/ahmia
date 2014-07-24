from django.db import models


class CrawledWebsite(models.Model):
    domain = models.CharField(max_length=255)
    url = models.URLField(max_length=255, unique=True)
    title = models.CharField(max_length=255)
    keywords = models.CharField(max_length=255)
    h1 = models.CharField(max_length=255)
    h2 = models.CharField(max_length=255)
    h3 = models.CharField(max_length=255)
    h4 = models.CharField(max_length=255)
    text = models.TextField()
    words = models.TextField()
