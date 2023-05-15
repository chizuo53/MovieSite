from django.core.management.base import BaseCommand

from muser.models import UserLike

from tool.models import Tool

class Command(BaseCommand):
    help = 'Update movies that users like'

    def handle(self, *args, **kwargs):
        userlikes_set = set()

        userlikes = UserLike.objects.values_list('like')
        for likes in userlikes:
            userlikes_set.update(likes[0])
        userlikes_list = list(userlikes_set)
        if userlikes_list:
            Tool.objects.mongo_update_one({'name':'movies_to_update'},{'$addToSet':{'testfield':{'$each':userlikes_list}}}, upsert=True)
