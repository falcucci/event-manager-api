from rest_framework import serializers
from events.models import Event

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = (
            'name',
            'description',
            'status',
            'start_date',
            'end_date',
            'location',
            'is_public',
            'created_at',
            'updated_at',
            'created_by',
            'subscribers'
        )
