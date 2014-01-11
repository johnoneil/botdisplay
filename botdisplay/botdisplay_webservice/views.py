# vim: set ts=2 expandtab:
# Create your views here.
from django.template import Context, loader
from botdisplay.botdisplay_webservice.models import URLDisplay
from django.http import HttpResponse

def index(request):
  urls_to_display = URLDisplay.objects.all()
  t = loader.get_template('botdisplay/index.html')
  c = Context({
    'urls_to_display': urls_to_display,
    })
  return HttpResponse(t.render(c))
