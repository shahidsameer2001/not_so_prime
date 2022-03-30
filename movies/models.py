from datetime import datetime
from django.db import models

# Create your models here.
class Movie(models.Model):
    id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 50)
    image = models.URLField()
    movie_url = models.URLField()
    uploaded = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class Series(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    image = models.URLField()
    uploaded = models.DateField(auto_now=True)

    def __str__(self):
        return self.name

class SeriesVideo(models.Model):
    series = models.ForeignKey(Series,on_delete=models.CASCADE)
    season = models.IntegerField()
    episode = models.IntegerField()
    video_url = models.URLField()
    uploaded = models.DateField(auto_now=True)

    def __str__(self):
        return self.series.name + " season "+str(self.season) + " E " + str(self.episode)


class Room(models.Model):
    name = models.CharField(max_length=1000)


class Message(models.Model):
    value = models.CharField(max_length=10000000)
    date = models.DateTimeField(default=datetime.now, blank=True)
    room = models.CharField(max_length=1000000)
    user = models.CharField(max_length=1000000)
