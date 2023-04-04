from django.db import IntegrityError
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from quiz.models import Student


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        fields = ['email', 'username', 'password', 'first_name', 'last_name', 'phone', 'birth_date']

    phone = serializers.IntegerField(allow_null=True, required=False)
    birth_date = serializers.DateTimeField(allow_null=True, required=False)

    def create(self, validated_data):
        try:
            user = self.perform_create(validated_data)
        except IntegrityError:
            self.fail("cannot_create_user")

        Student.objects.create(
            user=user
        )

        return user
