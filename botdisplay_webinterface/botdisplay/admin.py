# vim: set ts=2 expandtab:
from botdisplay.models import URLDisplay
from django.contrib import admin

class BotdisplayAdmin(admin.ModelAdmin):
	list_display = ('url', 'display_time', 'creation_date','created_by')

admin.site.register(URLDisplay, BotdisplayAdmin)
