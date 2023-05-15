from bson import ObjectId

from rest_framework import serializers

class ObjectIdField(serializers.Field):

    def __init__(self, **kwargs):
        kwargs['read_only'] = True
        super().__init__(**kwargs)

    def to_representation(self, value):
        return str(value)

    def to_internal_value(self, data):
        if ObjectId.is_valid(data):
            return ObjectId(data)
        raise ValidationError('Received an unvalid oid')
