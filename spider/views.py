from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAdminUser

from .models import Spider
from .serializers import SpiderSerializer
from .tasks import send_check_spider_email
from mutils.permissions import AccessSpider
from mutils.pagination import SpiderPageNumberPagination
from mutils.viewsets import MongoModelViewSet
from mutils.serializers import _movie_origin

# Create your views here.

class SpiderViewSet(MongoModelViewSet):

    serializer_class = SpiderSerializer
    pagination_class = SpiderPageNumberPagination
    permission_classes = [IsAdminUser, AccessSpider]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Spider.objects.all().order_by('-date_created')
        else:
            queryset = Spider.objects.filter(owner=self.request.user).order_by('-date_created')
        return queryset
        

    def perform_create(self, serializer):
        owner = self.request.user
        serializer.save(owner=owner, status='audit')
        if not owner.is_superuser:
            send_check_spider_email.delay(owner.pk, serializer.validated_data['code'])

    def perform_update(self, serializer):
        if not self.request.user.is_superuser and serializer.instance.status == 'audit' and serializer.validated_data.get('status', 'audit') != 'audit':
            raise ValidationError("You cannot change spider status when status is 'audit'")
        if serializer.validated_data.get('code', None) and serializer.validated_data['code'] != serializer.instance.code:
            if serializer.instance.status not in ['has_deleted', 'audit', 'ready']:
                raise ValidationError("You cannot change spider code when spider is running or spider data is not deleted")
            serializer.validated_data['status'] = 'audit'
        serializer.save()
        _movie_origin.pop(serializer.instance.spidername, None)
        if not self.request.user.is_superuser and serializer.validated_data['status'] == 'audit':
            send_check_spider_email.delay(self.request.user.pk, serializer.validated_data['code'])


