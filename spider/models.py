import os
from functools import partial
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

from djongo import models

# Create your models here.

class Spider(models.Model):
    status_choice = [('audit','audit'), ('start','start'), ('ready','ready'), ('running','running'), ('pause','pause'), ('resume','resume'), ('terminate','terminate'), ('error','error'), ('finished','finished'), ('has_paused','has_paused'), ('has_terminated','has_terminated'), ('restart','restart'), ('delete','delete'), ('has_deleted','has_deleted')]

    def default_stats():
        return {'movierate':0,'movielinkrate':0,'moviecount':0,'movielinkcount':0}

    _id = models.ObjectIdField()
    spidername = models.CharField(max_length=50)
    sitename = models.CharField(max_length=100)
    siteurl = models.URLField(max_length=300)
    owner = models.ForeignKey(User, related_name='spiders', on_delete=models.CASCADE)
    code = models.TextField()
    status = models.CharField(max_length=50, choices=status_choice)
    comment = models.TextField(blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    searchable = models.BooleanField(default=False)
    rate = models.IntegerField(default=settings.SPIDER_DEFAULT_RATE,validators=[MinValueValidator(settings.SPIDER_MIN_RATE), MaxValueValidator(settings.SPIDER_MAX_RATE)])
    stats = models.JSONField(default=default_stats, blank=True)
    available = models.BooleanField(default=True)

    class Meta:
        db_table = 'spider'
        managed = False
