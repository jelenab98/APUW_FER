from rest_framework import serializers
from .models import User, Quote


class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = "__all__"
        depth = 1   # prikazuje i podatke o autoru


class UserSerializer(serializers.ModelSerializer):
    #quote = QuoteSerializer(read_only=True, many=True)

    class Meta:
        model = User
        fields = "__all__"
