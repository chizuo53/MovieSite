from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAdminUser

from .models import Spider
from .serializers import SpiderSerializer
from mutils.misc import save_spider_code, write_code_to_py
from mutils.permissions import AccessSpider
from mutils.viewsets import MongoModelViewSet

# Create your views here.

class SpiderViewSet(MongoModelViewSet):

    serializer_class = SpiderSerializer
    permission_classes = [IsAdminUser, AccessSpider]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Spider.objects.all()
        else:
            queryset = Spider.objects.filter(owner=self.request.user)
        return queryset
        

    def perform_create(self, serializer):
        owner = self.request.user
        spidername = serializer.validated_data['spidername']
        code = serializer.validated_data['code']
        store_path = save_spider_code(spidername, code)
        serializer.save(owner=owner, store_path=store_path, status='audit')

    def perform_update(self, serializer):
        if not self.request.user.is_superuser and serializer.instance.status == 'audit' and serializer.validated_data.get('status', 'audit') != 'audit':
            raise ValidationError("You cannot change spider status when status is 'audit'")
        if 'code' in serializer.validated_data:
            store_path = serializer.instance.store_path
            code = serializer.validated_data['code']
            write_code_to_py(store_path, code)
        serializer.save()


