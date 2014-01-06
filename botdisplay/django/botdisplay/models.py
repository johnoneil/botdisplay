# vim: set ts=2 expandtab:
from django.db import models
from django.contrib.auth.models import User
import datetime

class URLDisplay(models.Model):
  url = models.CharField(max_length=2048)
  display_time = models.IntegerField()
  creation_date = models.DateTimeField('date published', auto_now_add=True)
  created_by = models.ForeignKey(User, related_name='+')
  def __unicode__(self):
    return self.url

