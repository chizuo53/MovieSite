from djongo import models

# Create your models here.

class Movie(models.Model):
    _id = models.ObjectIdField(db_column='_id')
    spidername = models.CharField(max_length=50, db_column='spidername')
    moviename = models.CharField(max_length=200, db_column='moviename')
    movieidentity = models.CharField(max_length=100, db_column='movieidentity')
    movieurl = models.CharField(max_length=300, db_column='movieurl')
    post = models.CharField(max_length=200, db_column='post')
    player = models.JSONField(db_column='player')
    created_time =  models.FloatField(db_column='created_time')

    objects = models.DjongoManager()

    class Meta:
        managed = False
        db_table = 'movie'

