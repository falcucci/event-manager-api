import json
from django.http import HttpResponse
from rest_framework import status

def health(request):
    return HttpResponse(
        json.dumps({"status": "ok"}),
        content_type="application/json",
        status=status.HTTP_200_OK
    )
