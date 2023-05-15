from collections import defaultdict

from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import Movie
from muser.models import UserLike
from tool.models import Tool
from .serializers import MovieSerializer, MoviePlayerSerializer
from spider.models import Spider
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

    @method_decorator(cache_page(60*30))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


class MovieSearchView(generics.ListAPIView):

    pagination_class = MoviePageNumberPagination
    serializer_class = MovieSerializer

    def get_cursor(self):
        moviename = self.request.query_params.get('m')
        regexm = f'.*{moviename}.*'
        cursor = Movie.objects.mongo_aggregate([{'$match':{'moviename':{'$regex':regexm}}}, {'$group':{'_id':'$moviename', 'time':{'$first':'$created_time'}, 'post':{'$first':'$post'}, 'count':{'$sum':1}}}])
        return cursor

    def get_queryset(self):
        return [c for c in self.get_cursor()]

    def list(self, request, *args, **kwargs):
        moviename = request.query_params.get('m')
        if int(request.query_params.get('rt', 0)) and moviename:
            moviename = request.query_params.get('m')
            if moviename:
                Tool.objects.mongo_update_one({'name':'movies_to_update'},{'$addToSet':{'funcfield':moviename}},upsert=True)
        return super().list(self, request, *args, **kwargs)

class MoviePlayerView(generics.ListAPIView):

    serializer_class = MoviePlayerSerializer

    def get_queryset(self):
        mname = self.request.query_params.get('m')
        queryset = Movie.objects.filter(moviename=mname)
        return queryset

    def list(self, request, *args, **kwargs):
        raw_response = super().list(request, *args, **kwargs)
        raw_data = raw_response.data
        if request.user and request.user.is_authenticated:
            try:
                ulike = UserLike.objects.get(user=request.user)
            except ObjectDoesNotExist:
                movielikes = []
            else:
                movielikes = ulike.like
            finally:
                moviename = request.query_params.get('m')
                like = moviename in movielikes
        else:
            like = False
        return Response({'like':like, 'playerlist':raw_data})

        

