# vim: set ts=2 expandtab:
from botdisplay.models import URLDisplay
from django.contrib import admin

class BotdisplayAdmin(admin.ModelAdmin):
	#list_display = ('url', 'display_time')
  exclude = ('created_by',)
  def save_model(self, request, obj, form, change):
    obj.created_by = request.user
    obj.save()

admin.site.register(URLDisplay, BotdisplayAdmin)
