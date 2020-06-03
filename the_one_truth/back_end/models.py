from django.db import models


class User(models.Model):
    _id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    register_date = models.DateTimeField(auto_now=True)
    last_login_time = models.DateTimeField(auto_now=True, null=True)
    group_id = models.IntegerField(default=0)
    friend_list = models.ManyToManyField('self', symmetrical=True)
    friend_num = models.IntegerField(default=0)
    
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
            'register_time': self.register_date,
            'last_login_time': self.last_login_time,
            'group_name': self.get_group_type(),
            'friend_list': self.get_friend_list()
        }
        return user_info


class Script(models.Model):
    script_id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    title = models.CharField(max_length=25, unique=True)
    add_time = models.DateTimeField(auto_now=True)
    # author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # history_script = models.ManyToManyField('self', related_name='script_history', symmetrical=False)
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
            'script_tittle': self.title,
            'player_num number': self.player_num,
            'truth': self.truth,
            'description': self.description,
            'murder': self.murder_id
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
    ready_status = models.IntegerField(default=0)

    class Meta:
        db_table = 'Player'

    def ready(self, tag):
        assert self.ready_status == tag - 1
        self.ready_status = tag
        self.save()
    
    def show_role_info(self):
        return {
            'player_id': self.player_id, 'name': self.user.name,
            'role_id': self.role_id, 'role_name': self.role.role_name,
            'background': self.role.background, 'timeline': self.role.timeline,
            'task': self.role.task, 'is_murder': self.role.is_murder
        }


class Clue(models.Model):
    clue_id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    script = models.ForeignKey(Script, related_name='clue_script', on_delete=models.CASCADE)
    clue_description = models.CharField(max_length=5000)
    text = models.CharField(max_length=50)

    player_list = models.ManyToManyField(Player, through='PlayerClue')

    class Meta:
        db_table = 'Clue'

    def show_clue(self):
        return {
            'text': self.text,
            'clue_id': self.clue_id,
            'description': self.clue_description
        }


class PlayerClue(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    clue = models.ForeignKey(Clue, on_delete=models.CASCADE)

    is_public = models.IntegerField(default=0)

    class Meta:
        db_table = 'Player_Clue_Relationship'


class Dialogue(models.Model):
    dialogue_id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    content = models.CharField(max_length=500, default='')

    room = models.ForeignKey(Room, related_name='dialogue_room', on_delete=models.CASCADE)
    player = models.ForeignKey(Player, related_name='dialogue_player', on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'Dialogue'