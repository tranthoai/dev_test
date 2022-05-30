from django.db import models
from django.contrib.auth.models import User


class Movie(models.Model):
    url = models.CharField(max_length=500)
    title = models.CharField(max_length=255)
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Vote(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    vote = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
