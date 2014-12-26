from rest_framework import serializers
from main.models import Link
from django.contrib.auth.models import User

class LinkSerializer(serializers.ModelSerializer):
	user_id = serializers.ReadOnlyField()

	class Meta:
		model = Link
		fields = ('pk', 'title', 'body', 'publish_date', 'user_id')


class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'password', 'last_login', 'first_name', 'last_name', 'username', 'email', 'is_staff', 'date_joined', )