# vim: set ts=2 expandtab:
from django.db import models
import datetime

class URLDisplay(models.Model):
  url = models.CharField(max_length=2048)
  display_time = models.IntegerField()
  creation_date = models.DateTimeField('date published')
  created_by = models.CharField(max_length=200)
  def __unicode__(self):
    return self.url
  def was_published_today(self):
    return self.creation_date.date() == datetime.date.today()

