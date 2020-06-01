from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json

from django.utils.timezone import now
import sys
import json

print(sys.path)

from . import models

# Create your views here.

def index(request):
    return HttpResponse('Hello, world!')


def test(request):
    msg = {"func": 'test'}
    return JsonResponse(msg)


def register_handler(request):
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        username = req['username']
        print(username)
        password = req['password']
        group_id = req['group_id']   # TODO: changed
        email = req['email']
        user = models.User.objects.filter(name=username)
        now_time = now()

        user_id, i = 0, 0
        new_user = models.User.objects.filter(_id=i).first()
        while new_user:
            i += 1
            new_user = models.User.objects.filter(_id=i).first()
        user_id = i
        
        if not user:
            models.User.objects.create(_id=user_id, name=username, password=password, email=email,
                                       group_id=group_id, register_date=now_time, friend_num=0,
                                       last_login_time=now_time)
        else:
            error = 'Username has been registered.'
        if error is None:
            response['error_num'] = 0
            data = {
                'name': username,
                'groupid': group_id,
                'reg_time': now_time,
                "last_login_time": 0,
            }
            response['data'] = data
        else:
            response['error_num'] = 1
            response['msg'] = error
    return JsonResponse(response)


def login_handler(request):
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        username = req['username']
        password = req['password']
        user = models.User.objects.filter(name=username).first()
        if not user:
            error = 'No such user.'
        else:
            psw = user.password
            if password != psw:
                error = 'Wrong password.'
        if error is None:
            response['error_num'] = 0
            data = {
                "username": username,
                "groupid": user.group_id,
                "last_login_time": user.last_login_time,
            }
            # user.update(last_login_time=now())
            response['data'] = data
        else:
            response['error_num'] = 1
            response['msg'] = error
    return JsonResponse(response)


def get_friend_list_request(request):
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        username = req['username']
        user = models.User.objects.filter(name=username).first()
        friend_list = user.get_friend_list()
        friend_name_list = [friend.name for friend in friend_list]
        data = {
            'friend_list': friend_name_list,
        }
        response['data'] = data
    return JsonResponse(response)


def add_friend_request(request):
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        username = req['username']
        user = models.User.objects.filter(name=username).first()
        user_to_be_add_name = req['name']
        user_to_be_add = models.User.objects.filter(name=user_to_be_add_name).first()
        if not user_to_be_add:
            error = 'No such user'
        else:
            user.friend_list.add(user_to_be_add)
            user_to_be_add.friend_list.add(user)
            user.friend_num += 1
            user_to_be_add.friend_num += 1
            user.save()
            user_to_be_add.save()
        if error is None:
            response['error_num'] = 0
        else:
            response['error_num'] = 1
            response['msg'] = error
    return JsonResponse(response)


def delete_friend_request(request):
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        username = req['username']
        user = models.User.objects.filter(name=username).first()
        user_to_be_delete_name = req['name']
        user_to_be_delete = models.User.objects.filter(name=user_to_be_delete_name).first()
        if not user_to_be_delete:
            error = 'No such user'
        else:
            user.friend_list.remove(user_to_be_delete)
            user_to_be_delete.friend_list.remove(user)
            user.friend_num -= 1
            user_to_be_delete.friend_num -= 1
            user.save()
            user_to_be_delete.save()
        if error is None:
            response['error_num'] = 0
        else:
            response['error_num'] = 1
            response['msg'] = error
    return JsonResponse(response)


def init_room(request):
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        num_person = req['num_person']
        
        room_id, i = 0, 0
        room = models.Room.objects.filter(room_id=i).first()
        while room:
            i += 1
            room = models.Room.objects.filter(room_id=i).first()
        # script_item = models.Script.objects.filter(script_id=0).first()
        room = models.Room.objects.create(room_id=i, size=num_person, stage=0, script_id=script_item)
        room_id = i

        if error is None:
            script = models.Script.objects.filter(player_num=num_person)
            script_name = [sc.title for sc in script]
            response['error_code'] = 0
            data = {
                "room_id": room_id,
                "script_to_select": script_name
            }
            response['data'] = data
        else:
            response['error_code'] = 1
            response['msg'] = error
        return JsonResponse(response)


def upsend_script(request):
    # update_role
    # update_clue
    # update_script
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        title = req['title']
        player_num = req['player_num']
        truth = req['truth']
        description = req['description']
        murder = req['murder_id']
        
        sc_id = 0
        script = models.Script.objects.filter(script_id=sc_id).first()
        while script:
            sc_id += 1
            script = models.Script.objects.filter(script_id=sc_id).first()
        script = models.Script.objects.create(script_id=sc_id, title=title, truth=truth, description=description,
                                              player_num=player_num, add_time=now(), murder_id=murder)

        if error is None:
            sc = models.Script.objects.filter(script_id=sc_id).first()
            ti = sc.title
            pn = sc.player_num
            tr = sc.truth
            des = sc.description
            mu = sc.murder_id
            data = {
                "script_tittle": ti,
                "player_num": pn,
                "truth": tr,
                "description": des,
                "murder": mu
            }
            response['data'] = data
        return JsonResponse(response)


def enter_room(request):
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        username = req['username']
        room_id = req['room_id']
        is_master = req['is_master']    ## TODO: add this request
        user = models.User.objects.filter(name=username).first()
        room = models.Room.objects.filter(room_id=room_id).first()

        player = models.Player.objects.filter(user_id_id=user._id).first()

        if not player:
            player_id, i = 0, 0
            player = models.Player.objects.filter(player_id=i).first()
            while player:
                i += 1
                player = models.Player.objects.filter(player_id=i).first()
            player = models.Player.objects.create(player_id=i, user_id=user, room_id=room, 
                                                is_master=is_master, role_id=None)
            player_id = i

        player_list = models.Player.objects.filter(room_id_id=room_id)
        room = models.Room.objects.filter(room_id=room_id).first()
        
        player_name_list, start, script_id = [], False, None
        if room.stage == 1:
            start = True
        script_id = room.script_id_id
        for player in player_list:
            player_name_list.append(player.user_id._id)
        if error is None:
            response['error_code'] = 0
            data = {
                "player_list": player_name_list,
                "start": start,
                "script_id": script_id        # TODO: change this return
            }
            response['data'] = data
        else:
            response['error_code'] = 1
            response['msg'] = error
        return JsonResponse(response)


def room_owner_choose_script(request):
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        room_id = req['room_id']
        script_title = req['script_title']      # TODO: this changed
        room = models.Room.objects.filter(room_id=room_id).first()
        room.script_id = models.Script.objects.filter(title=script_title).first()
        room.save()
        if error is None:
            response['error_code'] = 0
        else:
            response['error_code'] = 1
            response['msg'] = error
        return JsonResponse(response)


def start_game(request):
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        room_id = req['room_id']
        script_title = req['script_title']
        script = models.Script.objects.filter(title=script_title).first()
        room = models.Room.objects.filter(room_id=room_id).first()
        role_list = models.Role.objects.filter(script_id_id=script.script_id)
        truth = script.truth
        murder_role = models.Role.objects.filter(script_title=script_title, is_murder=1).first()
        
        role_id, role_name, background, timeline, task = [], [], [], [], []
        for role in role_list:
            role_id.append(role.role_id)
            role_name.append(role.role_name)
            background.append(role.background)
            timeline.append(role.timeline)
            task.append(role.task)
        clue_list = models.Clue.objects.filter(script_title=script_title)
        c_list, clue_id, clue_description = [], [], []
        for clue in clue_list:
            c_list.append(clue.text)
            clue_id.append(clue.clue_id)
            clue_description.append(clue.clue_description)
        
        room.update(stage=1, script_title=script_title)
        if error is None:
            script_title = script.title
            data = {
                "script_title": script_title,
                "role_id": role_id,
                "role_list": role_name,
                "background": background,
                "timeline": timeline,
                "task": task,
                "truth":truth,
                "murder_id": murder_role.role_id,
                "clue_id": clue_id,
                "clue_list": c_list,
                "clue_description": clue_description
            }
            response['error_code'] = 0
        else:

            response['error_code'] = 1
            response['msg'] = error
        return JsonResponse(response)


