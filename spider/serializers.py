from django.conf import settings
from rest_framework import serializers

from .models import Spider
from mutils.fields import ObjectIdField

class SpiderSerializer(serializers.ModelSerializer):

    status_change_allow = {'audit':('ready', 'start'),
                           'ready':('start',),
                           'running':('terminate', 'pause'),
                           'has_paused':('resume', 'terminate'),
                           'error':('restart','delete'),
                           'has_terminated':('restart','delete'),
                           'finished':('restart','delete')
        }

    _id = ObjectIdField()
    owner = serializers.ReadOnlyField(source='owner.username')
    status = serializers.CharField(allow_blank=False, default='audit')
    date_created = serializers.ReadOnlyField()
    date_updated = serializers.ReadOnlyField()
    comment = serializers.CharField(allow_blank=True, default='', required=False)
    rate = serializers.IntegerField(default=settings.SPIDER_DEFAULT_RATE, min_value=settings.SPIDER_MIN_RATE, max_value=settings.SPIDER_MAX_RATE, required=False)
    stats = serializers.JSONField(required=False)

    def validate_status(self, value):
        if not self.instance:
            if value != 'audit':
                raise serializers.ValidationError("Spider status only could be 'audit' when creating spider")
        else:
            old_status = self.instance.status
            if value != old_status and value not in self.status_change_allow[old_status]:
                raise serializers.ValidationError(f"Spider status '{old_status}' only could be changed to one of {self.status_change_allow[old_status]}")
        return value


    class Meta:
        model = Spider
        fields = ['_id', 'spidername', 'owner', 'sitename', 'siteurl', 'code', 'status', 'date_created', 'date_updated', 'comment', 'searchable', 'rate', 'stats', 'available']
