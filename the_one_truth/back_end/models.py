from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    add_time = models.DateTimeField(auto_now=True)
    last_login__time = models.DateTimeField(auto_now=True)
    group_id = models.IntegerField()
    friend_list = models.CharField(max_length=1000)
    friend_num = models.IntegerField()

    class Meta:
        db_table="User"

    def __unicode__(self):
        return self.name


class Script(models.Model):
    name = models.CharField(max_length=20)
    add_time = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.name
# Create your models here.

