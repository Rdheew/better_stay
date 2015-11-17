RATING_CHOICES = (
(0, 'None'),
(1, '*'),
(2, '**'),
(3, '***'),
(4, '****'),
(5, '*****'),
)
from django.core.urlresolvers import reverse
VISIBILITY_CHOICES = (
(0, 'Public'),
(1, 'Anonymous'),
)
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Hotel(models.Model):
  title = models.CharField(max_length=300)
  description = models.TextField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(User)
  visibility = models.IntegerField(choices=VISIBILITY_CHOICES, default=0)

  def __unicode__(self):
    return self.title

  def get_absolute_url(self):
    return reverse("hotel_detail", args=[self.id])

class Review(models.Model):
  hotel = models.ForeignKey(Hotel)
  user = models.ForeignKey(User)
  created_at = models.DateTimeField(auto_now_add=True)
  text = models.TextField()
  visibility = models.IntegerField(choices=VISIBILITY_CHOICES, default=0)
  rating = models.IntegerField(choices=RATING_CHOICES, default=0)

  def __unicode__(self):
    return self.text
  rating = models.IntegerField(choices=RATING_CHOICES, default=0)
class Vote(models.Model):
  user = models.ForeignKey(User)
  hotel = models.ForeignKey(Hotel, blank=True, null=True)
  review = models.ForeignKey(Review, blank=True, null=True)

  def __unicode__(self):
    return "%s upvoted" % (self.user.username)

