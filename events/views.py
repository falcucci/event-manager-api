from rest_framework.response import Response
from rest_framework import viewsets, status
from events.models import Event
from events.serializers import EventSerializer, EventCreateSerializer
from events.permissions import CustomPermissions
from rest_framework.decorators import action
from django.utils import timezone
from copy import copy

class EventsViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by('-id')
    serializer_class = EventSerializer
    permission_classes = (CustomPermissions,)
    def get_queryset(self):
        try:
            data = {}
            for i in self.request.query_params:
                data[i] = self.request.query_params[i]
            return self.queryset.filter(**data)
        except KeyError:
            return self.queryset

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

    @action(methods=['GET'], detail=False)
    def subscribed(self, request):
        subscriptions = request.user.subscriptions.all()
        subscriptions_serialized = EventSerializer(subscriptions, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=subscriptions_serialized.data
        )

    @action(methods=['GET'], detail=False)
    def mine(self, request):
        events = Event.objects.filter(created_by=request.user)
        events_serialized = EventSerializer(events, many=True)
        return Response(
            status=status.HTTP_200_OK,
            data=events_serialized.data
        )

    @action(methods=['POST'], detail=True)
    def subscribe(self, request, pk=None):
        event = self.get_object()

        if event.start_date < timezone.now():
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
                data={"detail": "Event has already started."}
            )

        event.subscribers.add(request.user)
        return Response(
            status=status.HTTP_200_OK,
            data={"detail": "Successful subscription."}
        )

    @action(methods=['POST'], detail=True)
    def unsubscribe(self, request, pk=None):
        event = self.get_object()
        if request.user in event.subscribers.all():
            event.subscribers.remove(request.user)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


