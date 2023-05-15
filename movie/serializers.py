from collections import defaultdict

from rest_framework import serializers

from mutils.serializers import MovieListSerializer

class MovieSerializer(serializers.Serializer):

    moviename = serializers.CharField(max_length=200, source='_id')
    post = serializers.CharField(max_length=200)
    count = serializers.IntegerField()


class MoviePlayerSerializer(serializers.Serializer):

    spidername = serializers.CharField(max_length=100)
    sitename = serializers.CharField(max_length=100, required=False)
    siteurl = serializers.CharField(max_length=200, required=False)
    movieurl = serializers.CharField(max_length=200)
    post = serializers.CharField(max_length=200)
    player = serializers.JSONField()

    class Meta:
        list_serializer_class = MovieListSerializer
