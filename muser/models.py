from djongo import models

from django.contrib.auth.models import User

# Create your models here.

class UserLike(models.Model):

    def default_like():
        return []

    _id = models.ObjectIdField(db_column='_id')
    user = models.OneToOneField(to=User, on_delete=models.CASCADE)
    like = models.JSONField(db_column='like', default=default_like)

    class Meta:
        managed = False
        db_table = 'userlike'
