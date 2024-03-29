from __future__ import unicode_literals
from future import standard_library
from future.builtins import int

from time import time

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from mezzanine.core.models import Displayable, Ownable
from mezzanine.generic.models import Rating
from mezzanine.generic.fields import RatingField, CommentsField

class Link(Displayable, Ownable):

    body = models.TextField(max_length=200)
    link = models.URLField(blank=True)
    rating = RatingField()
    comments = CommentsField()

    @models.permalink
    def get_absolute_url(self):
        return ("link_detail", (), {"slug": self.slug})

    @property
    def domain(self):
        return urlparse(self.link).netloc
		


class Profile(models.Model):

    user = models.OneToOneField("auth.User")
    website = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    karma = models.IntegerField(default=0, editable=False)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)


    def __unicode__(self):
        return "%s" % (self.user)


@receiver(post_save, sender=Rating)
def karma(sender, **kwargs):
    """
    Each time a rating is saved, check its value and modify the
    profile karma for the related object's user accordingly.
    Since ratings are either +1/-1, if a rating is being edited,
    we can assume that the existing rating is in the other direction,
    so we multiply the karma modifier by 2.
    """
    rating = kwargs["instance"]
    value = int(rating.value)
    if not kwargs["created"]:
        value *= 2
    content_object = rating.content_object
    if rating.user != content_object.user:
        queryset = Profile.objects.filter(user=content_object.user)
        queryset.update(karma=models.F("karma") + value)
