from django.db import models


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=256)


class Quote(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name="message", on_delete=models.SET_NULL, null=True)
