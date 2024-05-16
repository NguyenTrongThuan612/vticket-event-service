from rest_framework import serializers

class ImageValidator(serializers.Serializer):
    image = serializers.ImageField()