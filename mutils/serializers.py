from collections import defaultdict

from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnList

from spider.models import Spider

_movie_origin = defaultdict(dict)

class MovieListSerializer(serializers.ListSerializer):

    @property
    def data(self):
        ret = super(serializers.ListSerializer, self).data
        for d in ret:
            spname = d['spidername']
            if spname not in _movie_origin:
                sp = Spider.objects.get(spidername=spname)
                _movie_origin[spname]['sitename'] = sp.sitename
                _movie_origin[spname]['siteurl'] = sp.siteurl
                _movie_origin[spname]['available'] = sp.available

            d['sitename'] = _movie_origin[spname]['sitename']
            d['siteurl'] = _movie_origin[spname]['siteurl']
            d['available'] = _movie_origin[spname]['available']
            del d['spidername']
        return ReturnList(ret, serializer=self)

