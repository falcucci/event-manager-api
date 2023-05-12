from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from datetime import datetime, timedelta

from events.models import Event


class AccountTestCase(APITestCase):

    def setUp(self) -> None:
        self.host = 'http://127.0.0.1:8000'
        self.admin = User.objects.create_user(
            username="admin_test",
            first_name="Admin",
            last_name="Test",
            email="admin_test@event.com",
            password="admin@test_123",
            is_staff=True
        )

        self.admin2 = User.objects.create_user(
            username="admin2_test",
            first_name="Admin2",
            last_name="Test",
            email="admin2_test@event.com",
            password="admin@test_123",
            is_staff=True
        )

        self.user = User.objects.create_user(
            username="user_test",
            first_name="User",
            last_name="Test",
            email="user_test@event.com",
            password="user@test_123",
            is_staff=False
        )

        self.event = Event.objects.create(
            name='My Event asdf',
            description='This is my event',
            status='active',
            start_date=datetime.now() + timedelta(days=1),
            end_date=datetime.now() + timedelta(days=2),
            created_by=self.admin,
            location='Milan',
            capacity=20,
            is_public=True
        )

        self.event.created_by = self.admin
        self.event.subscribers.add(self.user)
        self.event.save()

        self.event_1 = Event.objects.create(
            name='My Event 1',
            description='This is my event',
            status='active',
            start_date=datetime.now() + timedelta(days=1),
            end_date=datetime.now() + timedelta(days=2),
            created_by=self.admin,
            location='Milan',
            capacity=20,
            is_public=True 
        )
        self.event_1.created_by = self.admin
        self.event_1.save()

        response = self.client.post(
            f'{self.host}/api/auth/login',
            {"username": "admin_test", "password": "admin@test_123"})
        self.admin_token = response.data["access"]
        #
        response = self.client.post(
            f'{self.host}/api/auth/login',
            {"username": "user_test", "password": "user@test_123"})
        self.user_token = response.data["access"]

    def test_get_list(self):
        response = self.client.get(
            f'{self.host}/api/events/',
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.data), 0)


    def test_get_list_filter(self):
        response = self.client.get(
            f'{self.host}/api/events/?name__icontains=my',
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(response.data), 0)

    def test_create_event(self):
        new_event = {
            "name": "My Event 1",
            "description": "This is my event",
            "status": "active",
            "start_date": datetime.now() + timedelta(days=1),
            "end_date": datetime.now() + timedelta(days=2),
            "created_by": self.admin,
            "location": "Milan",
            "capacity": 20,
            "is_public": True
        }

        response = self.client.post(
            f'{self.host}/api/events/',
            new_event,
            HTTP_AUTHORIZATION=f'Bearer {self.admin_token}'
        )
        result = Event.objects.filter(name=new_event["name"])

        self.assertTrue(result.exists())
        self.assertNotEqual(response.data, None)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['name'], new_event['name'])

    def test_subscribe(self):
        response = self.client.post(
            f'{self.host}/api/events/{self.event_1.id}/subscribe/',
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(len(self.user.subscriptions.all()), 0)
        self.assertTrue(self.event_1 in self.user.subscriptions.all())

    def test_list_subscribed(self):
        response = self.client.get(
            f'{self.host}/api/events/subscribed/',
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
        )
        result = self.user.subscriptions.all()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), len(result))

    def test_unsubscribe(self):
        response = self.client.post(
            f'{self.host}/api/events/{self.event.id}/unsubscribe/',
            HTTP_AUTHORIZATION=f'Bearer {self.user_token}'
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.event_1 in self.user.subscriptions.all())
