from django.test import TestCase, Client
from rest_framework import status

from app.models import Member, Session


class SignupTests(TestCase):
    def setUp(self):
        self.client = Client()

    def call(self, data, path):
        return self.client.post(
            data=data,
            path=path,

        )

    def test_input_missing(self):
        data = {
            "username": "test"
        }

        response = self.call(data, "/members/signup")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "password": "test"
        }

        response = self.call(data, "/members/signup")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {}

        response = self.call(data, "/members/signup")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_already_exists(self):
        username = "test"
        Member.objects.create(username=username, password="moein123")
        data = {
            "username": username,
            "password": "moein123"
        }

        response = self.call(data, "/members/signup")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_successful_signup(self):
        data = {
            "username": "test",
            "password": "moein123"
        }

        response = self.call(data, "/members/signup")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class LoginTests(TestCase):
    def setUp(self):
        self.client = Client()

    def call(self, data, path):
        return self.client.post(
            data=data,
            path=path,
        )

    def test_input_missing(self):
        data = {
            "username": "test"
        }

        response = self.call(data, "/members/login")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {
            "password": "test"
        }

        response = self.call(data, "/members/login")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        data = {}

        response = self.call(data, "/members/login")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_username_missing(self):
        data = {
            "username": "test",
            "password": "moein123"
        }

        response = self.call(data, "/members/login")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_password_missmatch(self):
        username = "test"
        password = "moein123"
        Member.objects.create(username=username, password=password)
        data = {
            "username": username,
            "password": "anotherRandomString"
        }

        response = self.call(data, "/members/login")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_successful_login(self):
        username = "test"
        password = "moein123"
        Member.objects.create(username=username, password=password)
        data = {
            "username": username,
            "password": password
        }

        response = self.call(data, "/members/login")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Session.objects.count(), 1)
        session = Session.objects.all()[0]
        self.assertEqual(session.token, response.json().get("token"))
