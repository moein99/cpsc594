from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import serializers, status

from app.models import Member, Session


class SignupParameters(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class LoginParameters(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class Signup(APIView):
    def post(self, request):
        serializer = SignupParameters(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        if Member.objects.filter(username=username).exists():
            return JsonResponse(
                data={"message": "Member already exists"},
                status=status.HTTP_403_FORBIDDEN
            )

        Member.objects.create(username=username, password=password)
        return JsonResponse(
            data={"message": "Member created successfully"},
            status=status.HTTP_201_CREATED
        )


class Login(APIView):
    def post(self, request):
        serializer = LoginParameters(data=request.data)
        serializer.is_valid(raise_exception=True)

        member = Member.objects.filter(username=serializer.validated_data["username"]).first()
        if member is None:
            return JsonResponse(
                data={"message": "Username is missing"},
                status=status.HTTP_404_NOT_FOUND
            )

        if member.password != serializer.validated_data["password"]:
            return JsonResponse(
                data={"message": "Password is incorrect"},
                status=status.HTTP_403_FORBIDDEN
            )

        session = Session.objects.create(member=member)
        return JsonResponse(
                data={
                    "message": "Login was successful",
                    "token": session.token
                },
                status=status.HTTP_200_OK
            )
