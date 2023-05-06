import json
from django.http import HttpResponse

def health(request):
    return HttpResponse(
        json.dumps({"status": "ok"}),
        content_type="application/json"
    )
