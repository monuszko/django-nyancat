from uuid import uuid4

from django.db import models
from django.core.urlresolvers import reverse
from django.core.signing import (TimestampSigner, 
        BadSignature, SignatureExpired) # PEP 0328


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
        return str(self.url)

    def make_token(self):
        return TimestampSigner().sign(self.url)

    def restore_cookie_url(self):
        url, token = self.make_token().split(':', 1)
        return reverse('nyancat:restore_cookie',
                kwargs={'person_url': url, 'token': token,})

    def check_token(self, token):
        try:
            key = '%s:%s' % (self.url, token)
            TimestampSigner().unsign(key, max_age=60 * 60 * 48) # 2 days
        except (BadSignature, SignatureExpired):
            return False
        return True

