from django.db import models


class User(models.Model):
    _id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    register_date = models.DateTimeField(auto_now=True)
    last_login_time = models.DateTimeField(auto_now=True)
    group_id = models.IntegerField(null=True)
    friend_list = models.ManyToManyField('self', symmetrical=True, null=True)
    friend_num = models.IntegerField(null=True)
    
    class Meta:
        db_table = 'User'

    def get_friend_list(self):
        return self.friend_list.all()
    
    def get_group_type(self):
        return 'manager' if self.group_id == 1 else 'civilian'
    
    def show_user_info(self):
        user_info = {
            'name': self.name,
            'email': self.email,
            'register date': self.register_date,
            'user group': self.get_group_type(),
            'friend list': self.get_friend_list()
        }
        return user_info


class Script(models.Model):
    script_id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    title = models.CharField(max_length=25, unique=True)
    add_time = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
<<<<<<< HEAD
    history_script_id = models.ManyToManyField('self', related_name='script_id_history', symmetrical=False)
=======
    history_script = models.ManyToManyField('self', related_name='script_history', symmetrical=False)
>>>>>>> c0e94df44d76745807d8603ba2f3d8abe14c7aaa
    player_num = models.IntegerField(null=True)
    description = models.CharField(max_length=5000, default='')
    truth = models.CharField(max_length=100, default='')

    murder_id = models.IntegerField(null=True)

    class Meta:
        db_table = 'Script'

    def get_history_scripts(self):
        return self.history_script_id.all()
    
    def show_script_info(self):
        script_info = {
            'title': self.title,
            'player number': self.player_num,
            'description': self.description,
            'auther name': self.author_name,
            'history scripts': self.get_history_scripts(),
            'add time': self.add_time
        }
        return script_info


class Room(models.Model):
    room_id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    size = models.IntegerField(null=True)
    stage = models.IntegerField(default=0)
    script = models.ForeignKey(Script, related_name='room_script', on_delete=models.PROTECT, null=True)

    class Meta:
        db_table = 'Room'


class Role(models.Model):
    role_id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    role_name = models.CharField(max_length=20, default='')
    script = models.ForeignKey(Script, related_name='role_script', on_delete=models.CASCADE)
    
    is_murder = models.IntegerField(default=0)
    task = models.CharField(max_length=200, default='')
    background = models.CharField(max_length=200, default='')
    timeline = models.CharField(max_length=200, default='')
    
    role_description = models.CharField(max_length=5000, default='')

    class Meta:
        db_table = 'Role'

    def show_info(self, level):
        info = {
            'script id': self.script_id,
            'role description': self.role_description
        }
        if level == 'self':
            info['task'] = self.task
            info['is_murder'] = self.is_murder
        return info


class Player(models.Model):
    player_id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    user = models.ForeignKey(User, related_name='player_user', on_delete=models.CASCADE)
    role = models.ForeignKey(Role, related_name='player_role', on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, related_name='player_room', on_delete=models.CASCADE)
    is_master = models.IntegerField(default=0)
    movement_point = models.IntegerField(default=0)
    ready_1 = models.IntegerField(default=0)
    ready_2 = models.IntegerField(default=0)
    ready_3 = models.IntegerField(default=0)

    class Meta:
        db_table = 'Player'

    def ready(self, tag):
        if tag == 1:
            assert self.ready_1 == 0
            self.ready_1 = 1
        elif tag == 2:
            assert self.ready_1 == 1 and self.ready_2 == 0
            self.ready_2 = 1
        elif tag == 3:
            assert self.ready_1 + self.ready_2 == 2 and self.ready_3 == 0
            self.ready_3 = 1


class Clue(models.Model):
    clue_id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    script = models.ForeignKey(Script, related_name='clue_script', on_delete=models.CASCADE)
    clue_description = models.CharField(max_length=5000)
    text = models.CharField(max_length=50)

    player_list = models.ManyToManyField(Player, null=True, through='PlayerClue')

    class Meta:
        db_table = 'Clue'

    def show_clue(self):
        return {
            'script id': self.script_id,
            'clue info': self.clue_description
        }


class PlayerClue(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    clue = models.ForeignKey(Clue, on_delete=models.CASCADE)

    is_public = models.IntegerField(default=0)

    class Meta:
        db_table = 'Player_Clue_Relationship'


