from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)


class Quote(models.Model):
    message = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
