from django.db import models


class User(models.Model):
    name = models.CharField(max_length=20,primary_key=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    add_time = models.DateTimeField(auto_now=True)
    last_login_time = models.DateTimeField(auto_now=True)
    group_id = models.IntegerField(null = True)
    friend_list = models.CharField(max_length=1000, null = True)
    friend_num = models.IntegerField(null = True)
    class Meta:
        db_table="User"
    def __unicode__(self):
        return self.name


class game_role(models.Model):
    role_ID = models.DecimalField(max_digits=20,decimal_places=0,primary_key=True, default = 0)
    #script_title = models.ForeignKey("script",related_name='title',on_delete=models.PROTECT)
    script_ID = models.DecimalField(max_digits = 20, decimal_places = 0, default = '')
    role_name = models.CharField(max_length=50)
    task = models.CharField(max_length=200)
    role_description = models.CharField(max_length=5000)
class script(models.Model):
    title = models.CharField(max_length=50,default='')
    script_ID = models.DecimalField(max_digits=20,decimal_places=0,primary_key = True,default='')
    add_time = models.DateTimeField(auto_now=True)
    player_num = models.IntegerField(null = True)
    muder_role_id = models.ForeignKey(game_role, on_delete = models.PROTECT, null = True)
    truth = models.CharField(max_length=100,default='')
    description = models.CharField(max_length=5000,default='None')
    def __unicode__(self):
        return self.title


class game_user(models.Model):
    user_ID = models.DecimalField(max_digits=20,decimal_places=0,primary_key=True)
    pass_word = models.CharField(max_length=15)
    user_name = models.ForeignKey(User,on_delete=models.PROTECT)
    remark = models.CharField(max_length=20)
    user_level = models.IntegerField(null = True)
    email = models.CharField(max_length=50)
    register_date = models.DateField()
    last_login_time = models.DateTimeField()
    def __unicode__(self):
        return self.user_ID

class game_clue(models.Model):
    clue_ID = models.DecimalField(max_digits=20,decimal_places=0,primary_key=True)
    script_title = models.ForeignKey(script,on_delete=models.PROTECT)
    clue_description = models.CharField(max_length=5000)
    def __unicode__(self):
        return self.clue_ID


class game_room(models.Model):
    room_ID = models.DecimalField(max_digits=20,decimal_places=0,primary_key=True)
    size = models.IntegerField(null = True)
    stage = models.CharField(max_length=50)
    script_title = models.ForeignKey(script,on_delete=models.PROTECT)

class player(models.Model):
    player_ID = models.DecimalField(max_digits=20,decimal_places=0,primary_key=True)
    user_id = models.ForeignKey(game_user,on_delete=models.PROTECT)
    room_id = models.ForeignKey(game_room,on_delete=models.CASCADE)
    #role_id = models.ForeignKey(game_role,on_delete=models.PROTECT)
    ready_1 = models.IntegerField(default=0)
    ready_2 = models.IntegerField(default=0)
    ready_3 = models.IntegerField(default=0)

class player_clue(models.Model):
    player_ID = models.ForeignKey(player,on_delete = models.CASCADE)
    clue_ID = models.ForeignKey(game_clue,on_delete = models.PROTECT)
    room_ID = models.ForeignKey(game_room,on_delete = models.CASCADE)
