import uuid

from django.db import models


class Member(models.Model):
    username = models.CharField(max_length=40, primary_key=True)
    password = models.CharField(max_length=40)


class Session(models.Model):
    token = models.CharField(max_length=40, default=uuid.uuid4)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
