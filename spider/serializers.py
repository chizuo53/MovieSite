from rest_framework import serializers

from .models import Spider
from mutils.fields import ObjectIdField

class SpiderSerializer(serializers.ModelSerializer):

    status_change_allow = {'audit':('ready', 'start'),
                           'ready':('start',),
                           'running':('terminate', 'pause'),
                           'has_paused':('resume',),
                           'error':('restart',),
                           'has_terminated':('restart',),
                           'finished':('restart',)
        }

    _id = ObjectIdField()
    owner = serializers.ReadOnlyField(source='owner.username')
    date_created = serializers.ReadOnlyField()
    date_updated = serializers.ReadOnlyField()

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
        fields = ['_id', 'spidername', 'owner', 'sitename', 'siteurl', 'code', 'status', 'date_created', 'date_updated', 'comment']
