from django.db import models


class User(models.Model):
    _id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    register_date = models.DateField(auto_now=True, auto_now_add=True)
    last_login_time = models.DateTimeField(auto_now=True, auto_now_add=True)
    group_id = models.IntegerField(null=True)
    friend_list = models.ManyToManyField('self', related_name='name', symmetrical=True)
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
    add_time = models.DateTimeField(auto_now=True, auto_now_add=True)
    author_name = models.ForeignKey('User', related_name='name', on_delete=models.SET_NULL)
    history_script_id = models.ManyToManyField('self', related_name='script_id', symmetrical=False)
    player_num = models.IntegerField(null=True)
    title = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=5000, default='', unique=True)
    truth = models.CharField(max_length=100, default='')

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
    stage = models.CharField(max_length=50)
    script_title = models.ForeignKey('Script', related_name='title', on_delete=models.PROTECT)


class Player(models.Model):
    player_id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    user_id = models.ForeignKey('User', related_name='_id', on_delete=models.CASCADE)
    role_id = models.ForeignKey('Role', related_name='role_id', on_delete=models.SET_NULL)
    room_id = models.ForeignKey('Room', related_name='room_id', on_delete=models.CASCADE)
    is_master = models.IntegerField(default=0)
    movement_point = models.IntegerField(default=0)
    ready_1 = models.IntegerField(default=0)
    ready_2 = models.IntegerField(default=0)
    ready_3 = models.IntegerField(default=0)

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
    script_title = models.ForeignKey('Script', related_name='title', on_delete=models.CASCADE)
    clue_description = models.CharField(max_length=5000)

    def show_clue(self):
        return {
            'script title': self.script_title,
            'clue info': self.clue_description
        }


class Role(models.Model):
    role_id = models.DecimalField(max_digits=20, decimal_places=0, primary_key=True)
    script_title = models.ForeignKey('Script', related_name='title', on_delete=models.CASCADE)
    is_murder = models.IntegerField(default=0)
    task = models.CharField(max_length=200, default='')
    role_description = models.CharField(max_length=5000, default='')

    class Meta:
        db_table = 'Role'

    def show_info(self, level):
        info = {
            'script title': self.script_title,
            'role description': self.role_description
        }
        if level == 'self':
            info['task'] = self.task
            info['is_murder'] = self.is_murder
        return info

