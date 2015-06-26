from uuid import uuid4

from django.db import models
from django.core.urlresolvers import reverse


class Video(models.Model):
    url = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return str(self.url)

    def get_youtube_url(self):
        return 'https://www.youtube.com/watch?v=%s' % self.url


class Person(models.Model):
    password = models.CharField(max_length=32, unique=True, 
            default=str(uuid4()).replace('-', ''))
    url = models.CharField(max_length=32, unique=True, 
            default=str(uuid4()).replace('-', ''))
    videos = models.ManyToManyField(Video)
    email = models.EmailField(blank=True)

    def get_absolute_url(self):
        return reverse('nyancat:my_videos', kwargs={'person_url': self.url})

    def __str__(self):
        return str(self.pk)

