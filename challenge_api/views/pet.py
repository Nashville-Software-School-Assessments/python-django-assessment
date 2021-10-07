from rest_framework import viewsets, serializers


class PetSerializer(serializers.ModelSerializer):
    """The Pet Serializer - Add your code below this line"""


class PetView(viewsets.ViewSet):
    """The Pet View class - Add your code below this line"""
    