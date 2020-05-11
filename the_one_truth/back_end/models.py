from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    add_time = models.DateTimeField(auto_now=True)
    last_login_time = models.DateTimeField(auto_now=True)
    group_id = models.IntegerField()
    friend_list = models.CharField(max_length=1000)
    friend_num = models.IntegerField()

    class Meta:
        db_table="User"

    def __unicode__(self):
        return self.name


class script(models.Model):
    title = models.CharField(max_length=50,primary_key=True,default='')
    script_ID = models.DecimalField(max_digits=20,decimal_places=0,default='')
    add_time = models.DateTimeField(auto_now=True)
    truth = models.CharField(max_length=100,default='')
    description = models.CharField(max_length=500,default='None')
    def __unicode__(self):
        return self.title


class game_user(models.Model):
    user_ID = models.DecimalField(max_digits=20,decimal_places=0,primary_key=True)
    pass_word = models.CharField(max_length=15)
    user_name = models.ForeignKey(User,on_delete=models.PROTECT)
    remark = models.CharField(max_length=20)
    user_level = models.IntegerField()
    email = models.CharField(max_length=50)
    register_date = models.DateField()
    last_login_time = models.DateTimeField()
    def __unicode__(self):
        return self.user_ID

class game_clue(models.Model):
    clue_ID = models.DecimalField(max_digits=20,decimal_places=0,primary_key=True)
    script_title = models.ForeignKey(script,on_delete=models.PROTECT)
    clue_description = models.CharField(max_length=500)
    def __unicode__(self):
        return self.clue_ID
class game_role(models.Model):
    role_ID = models.DecimalField(max_digits=20,decimal_places=0,primary_key=True)
    script_title = models.ForeignKey(script,on_delete=models.PROTECT)
    role_name = models.CharField(max_length=50)
    task = models.CharField(max_length=200)
    role_description = models.CharField(max_length=500)

class game_room(models.Model):
    room_ID = models.DecimalField(max_digits=20,decimal_places=0,primary_key=True)
    size = models.IntegerField()
    stage = models.CharField(max_length=50)
    script_title = models.ForeignKey(script,on_delete=models.PROTECT)
class player(models.Model):
    player_ID = models.DecimalField(max_digits=20,decimal_places=0,primary_key=True)
    user_id = models.ForeignKey(game_user,on_delete=models.PROTECT)
    room_id = models.ForeignKey(game_room,on_delete=models.PROTECT)
    role_id = models.ForeignKey(game_role,on_delete=models.PROTECT)
