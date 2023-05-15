from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from rest_framework.views import Response, status
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets

from movie.models import Movie
from mutils.permissions import AccessUser
from mutils.pagination import UserPageNumberPagination, UserLikePageNumberPagination
from .serializers import StaffSerializer, SuperuserSerializer, UserLikeSerializer
from .models import UserLike

# Create your views here.

class CustomAuthToken(ObtainAuthToken):
    def post(self, request,*args,**kwargs):
        serializer =self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'pk': user.pk,
            'username':user.username,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })


class UserViewSet(viewsets.ModelViewSet):

    pagination_class = UserPageNumberPagination
    permission_classes = [IsAuthenticated, AccessUser]

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return SuperuserSerializer
        elif self.request.user.is_staff:
            return StaffSerializer

    def get_queryset(self):
        queryset = User.objects.all().order_by('pk')
        return queryset

    @action(detail=False, methods=['get'], url_path='level', name='user_level')
    def user_level(self, request):
        user = request.user
        return Response({
            'pk': user.pk,
            'username':user.username,
            'is_staff': user.is_staff,
            'is_superuser': user.is_superuser,
        })

    @action(detail=False, methods=['get'], url_path='like', name='user_like')
    def user_like(self, request):
        try:
            ulike = UserLike.objects.get(user=request.user)
        except ObjectDoesNotExist:
            like = []
        else:
            like = ulike.like
        finally:
            cursor = Movie.objects.mongo_aggregate([{'$match':{'moviename':{'$in':like}}}, {'$group':{'_id':'$moviename', 'time':{'$first':'$created_time'}, 'post':{'$first':'$post'}, 'count':{'$sum':1}}}])
            mlike = []
            for c in cursor:
                c['moviename'] = c['_id']
                mlike.append(c)
            paginator = UserLikePageNumberPagination()
            page = paginator.paginate_queryset(mlike, request, view=self)
            serializer = UserLikeSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

    @user_like.mapping.put
    def user_like_put(self, request):
        moviename = request.data['moviename']
        movies = Movie.objects.filter(moviename=moviename)
        if not movies:
            return Response({'detail':f'Movie: {moviename} does not exist'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            ulike = UserLike.objects.get(user=request.user)
        except ObjectDoesNotExist:
            like = [moviename]
            UserLike.objects.create(user=request.user, like=like)
        else:
            like = set(ulike.like)
            like.add(moviename)
            ulike.like = list(like)
            ulike.save()
        finally:
            return Response({'data':request.data}, status=status.HTTP_200_OK)

    @user_like.mapping.delete
    def user_like_delete(self, request):
        moviename = request.data['moviename']
        try:
            ulike = UserLike.objects.get(user=request.user)
        except ObjectDoesNotExist:
            pass
        else:
            like = set(ulike.like)
            like.discard(moviename)
            ulike.like = list(like)
            ulike.save()
        finally:
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'], url_path='movieinlike', name='movie_in_like')
    def movie_in_like(self, request):
        try:
            ulike = UserLike.objects.get(user=request.user)
        except ObjectDoesNotExist:
            movielikes = []
        else:
            movielikes = ulike.like
        finally:
            movie = request.query_params.get('m')
            like = movie in movielikes
            return Response({
                'pk': request.user.pk,
                'like': like
            })
