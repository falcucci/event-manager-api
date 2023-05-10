from rest_framework.response import Response
from rest_framework import viewsets, status
from events.models import Event
from events.serializers import EventSerializer, EventCreateSerializer
from events.permissions import CustomPermissions
from copy import copy

class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = (CustomPermissions,)

    def retrieve(self, request, pk=None):
        event = Event.objects.get(id=pk)
        serialized = EventSerializer(event)
        if event.created_by != request.user:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={
                    'message': 'You are not allowed to see this event.'
                }
            )
        return Response(
            status=status.HTTP_200_OK,
            data=serialized.data
        )

    def create(self, request, *args, **kwargs):
        data = copy(self.request.data)
        data['created_by'] = self.request.user.id
        serialized = EventCreateSerializer(data=data)
        if not serialized.is_valid():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data=serialized.errors
            )

        serialized.save()
        return Response(
            status=status.HTTP_201_CREATED,
            data=serialized.data
        )

    def update(self, request, pk=None):
        event = Event.objects.get(id=pk)
        if event.created_by != request.user:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
                data={
                    'message': 'You are not allowed to edit this event.'
                }
            )
        return super().update(request, pk)
