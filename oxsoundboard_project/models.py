from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from django.db import models

# Create your models here.
class Sound(models.Model):
    filename = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    person = models.CharField(max_length=255, default=None, null=True, blank=True)
    description = models.CharField(max_length=255)
    video_url = models.CharField(max_length=255, default=None)
    num_plays = models.IntegerField(default=0)
    rank = models.BooleanField(default=True)

    def __str__(self):
        return self.filename

    class Meta:
        ordering = ('-num_plays',)

    def get_absolute_url(self):
        return reverse('oxsound', kwargs={'filename': self.filename})
