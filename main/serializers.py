from rest_framework import serializers
from main.models import Link

class LinkSerializer(serializers.Serializer):
    pk = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=50)
    body = serializers.