from collections import defaultdict

from rest_framework import serializers
from rest_framework.utils.serializer_helpers import ReturnList

from spider.models import Spider

class MovieListSerializer(serializers.ListSerializer):

    movie_origin = defaultdict(dict)

    @property
    def data(self):
        ret = super(serializers.ListSerializer, self).data
        for d in ret:
            spname = d['spidername']
            if spname not in self.movie_origin:
                sp = Spider.objects.get(spidername=spname)
                self.movie_origin['spname']['name'] = sp.sitename
                self.movie_origin['spname']['url'] = sp.siteurl
            d['sitename'] = self.movie_origin['spname']['name']
            d['siteurl'] = self.movie_origin['spname']['url']
            del d['spidername']
        return ReturnList(ret, serializer=self)

