from djongo import models

# Create your models here.

class Tool(models.Model):
    _id = models.ObjectIdField(db_column='_id')
    name = models.CharField(max_length=100, db_column='name')
    funcfield = models.JSONField(db_column='funcfield')

    objects = models.DjongoManager()

    class Meta:
        managed = False
        db_table = 'tool'
