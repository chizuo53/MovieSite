from collections import defaultdict

from rest_framework import generics

from .models import Movie
from .serializers import MovieSerializer, MoviePlayerSerializer
from spider.models import Spider
from mutils.mixins import AddSiteMsgMixin
from mutils.pagination import MoviePageNumberPagination

# Create your views here.

class MovieListView(generics.ListAPIView):

    pagination_class = MoviePageNumberPagination
    serializer_class = MovieSerializer

    def get_cursor(self):
        cursor = Movie.objects.mongo_aggregate([{'$sort':{'created_time':1}}, {'$group':{'_id':'$moviename', 'time':{'$first':'$created_time'}, 'post':{'$first':'$post'}, 'count':{'$sum':1}}}, {'$sort':{'time':1}}])
        return cursor

    def get_queryset(self):
        return [c for c in self.get_cursor()]


class MovieSearchView(generics.ListAPIView):

    pagination_class = MoviePageNumberPagination
    serializer_class = MovieSerializer

    def get_cursor(self):
        mname = self.request.query_params.get('m')
        regexm = f'.*{mname}.*'
        cursor = Movie.objects.mongo_aggregate([{'$match':{'moviename':{'$regex':regexm}}}, {'$group':{'_id':'$moviename', 'time':{'$first':'$created_time'}, 'post':{'$first':'$post'}, 'count':{'$sum':1}}}])
        return cursor

    def get_queryset(self):
        return [c for c in self.get_cursor()]

class MoviePlayerView(generics.ListAPIView):

    serializer_class = MoviePlayerSerializer

    def get_queryset(self):
        mname = self.request.query_params.get('m')
        queryset = Movie.objects.filter(moviename=mname)
        return queryset

