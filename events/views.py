from rest_framework import viewsets
from events.models import Event
from events.serializers import EventSerializer
from events.permissions import CustomPermissions

class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (CustomPermissions,)
