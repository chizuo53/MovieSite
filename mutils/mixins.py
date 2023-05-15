from collections import defaultdict

class AddSiteMsgMixin:
    movie_origin = defaultdict(dict)

    def add_site_message(self):
        cursor = self.get_cursor()
        queryset = []
        for c in cursor:
            spname = c['spidername']
            if spname not in self.movie_origin:
                sp = Spider.objects.get(spidername=spname)
                movie_origin[spname]['name'] = sp.sitename
                movie_origin[spname]['url'] = sp.siteurl
            c['sitename'] = movie_origin[spname]['name']
            c['siteurl'] = movie_origin[spname]['url']
            queryset.append(c)
        return queryset

    def get_queryset(self):
        return self.add_site_message()
