# vim: set ts=2 expandtab:
from django.contrib import admin
from botdisplay.botdisplay_webservice.models import URLDisplay

class BotdisplayAdmin(admin.ModelAdmin):
  exclude = ('created_by',)
  def save_model(self, request, obj, form, change):
    obj.created_by = request.user
    obj.save()

admin.site.register(URLDisplay, BotdisplayAdmin)
