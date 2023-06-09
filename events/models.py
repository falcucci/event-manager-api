from django.contrib.auth.models import User
from datetime import datetime, timedelta
from django.db import models

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=100)
    start_date = models.DateTimeField(default=datetime.now() + timedelta(days=1))
    end_date = models.DateTimeField(default=datetime.now() + timedelta(days=2))
    location = models.CharField(max_length=100)
    capacity = models.IntegerField(default=20)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='event_created_by'
    )
    subscribers = models.ManyToManyField(
        User,
        related_name='subscriptions',
        blank=True
    )

    def __str__(self):
        return self.name
