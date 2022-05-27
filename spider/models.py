import os
from functools import partial
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from djongo import models

# Create your models here.

class Spider(models.Model):
    status_choice = [('audit','audit'), ('start','start'), ('ready','ready'), ('running','running'), ('pause','pause'), ('resume','resume'), ('terminate','terminate'), ('error','error'), ('finished','finished'), ('has_paused','has_paused'), ('has_terminated','has_terminated')]

    _id = models.ObjectIdField()
    spidername = models.CharField(max_length=50)
    sitename = models.CharField(max_length=100)
    siteurl = models.URLField(max_length=300)
    owner = models.ForeignKey(User, related_name='spiders', on_delete=models.CASCADE)
    code = models.TextField()
    store_path = models.CharField(max_length=200)
    status = models.CharField(max_length=50, choices=status_choice)
    comment = models.CharField(max_length=500)
    date_created = models.DateTimeField(auto_now=True)
    date_updated = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'spider'
        managed = False
