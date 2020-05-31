from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json

from django.utils.timezone import now
import sys

print(sys.path)

from . import models

from . import models

# Create your views here.


def test(request):
    msg = {"func": 'test'}
    return JsonResponse(msg)


def register_handler(request):
    if request.method == 'POST':
        response = {}
        error = None
        username = request.POST.get("username", None)
        print(username)
        password = request.POST.get("password", None)
        email = request.POST.get("email", None)
        user = models.User.objects.filter(name=username)
        now_time = now()
        if not user:
            models.User.objects.create(name=username, password=password, email=email,
                                       group_id=2, register_date=now_time, friend_num=0,
                                       last_login_time=now_time, friend_list=None)
        else:
            error = 'Username has been registered.'
        if error is None:
            response['error_num'] = 0
            data = {
                'name': username,
                'groupid': 2,
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
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
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
                "name": "pku",
                "groupid": 2,
                "last_login_time": user.last_login__time,
            }
            user.update(last_login_time=now())
            response['data'] = data
        else:
            response['error_num'] = 1
            response['msg'] = error
    return JsonResponse(response)


def get_friend_list_request(request):
    if request.method == 'POST':
        response = {}
        error = None
        username = request.POST.get("username", None)
        user = models.User.objects.filter(name=username)
        friend_list = user.get_friend_list()
        data = {
            'friend_list': friend_list,
        }
        response['data'] = data
    return JsonResponse(response)


def add_friend_request(request):
    if request.method == 'POST':
        response = {}
        error = None
        username = request.POST.get("username", None)
        user = models.User.objects.filter(name=username)
        user_to_be_add_name = request.POST.get("name", None)
        user_to_be_add = models.User.objects.filter(name=user_to_be_add_name)
        if not user_to_be_add:
            error = 'No such user'
        else:
            user.friend_list.add(user_to_be_add)
            user_to_be_add.friend_list.add(user)
            user.update(friend_num=user.friend_num + 1)
            user_to_be_add.update(friend_num=user_to_be_add.friend_num + 1)
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
        username = request.POST.get("username", None)
        user = models.User.objects.filter(name=username)
        user_to_be_delete_name = request.POST.get("name", None)
        user_to_be_delete = models.User.objects.filter(name=user_to_be_delete_name)
        if not user_to_be_delete:
            error = 'No such user'
        else:
            user.friend_list.remove(user_to_be_delete)
            user_to_be_delete.friend_list.remove(user)
            user.update(friend_num=user.friend_num - 1)
            user_to_be_add.update(friend_num=user_to_be_add.friend_num - 1)
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
        room_name = req['room_name']
        uid = req['user_id']
        
        room_id, i = 0, 0
        room = models.Room.objects.filter(room_id=i).first()
        while room:
            i += 1
            room = models.Room.objects.filter(room_id=i).first()
        room = models.Room.create(room_id=i, size=num_person, stage=0, script_title=None)
        room_id = i

        if error is None:
            script = models.Script.objects.filter(player_num=num_person)
            script_name = None
            for sc in script:
                script_name.append(sc.tittle)
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


def enter_room(request):
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        username = req['username']
        room_id = req['room_id']
        is_master = req['is_master']    ## TODO: add this request
        user = models.User.objects.filter(name=username).first()

        player_id, i = 0, 0
        player = models.Player.objects.filter(player_id=i).first()
        while player:
            i += 1
            player = models.Player.objects.filter(player_id=i).first()
        player = models.Player.create(player_id=i, user_id=user._id, room_id=room_id, 
                                      is_master=is_master, role_id=None)
        player_id = i

        player_list = models.Player.objects.filter(room_id=room_id)
        room = models.Room.objects.filter(room_id=room_id).first()
        
        player_name_list, start, script_title = [], False, None
        if room.stage == 1:
            start = True
            script_title = room.script_title
        for player in player_list:
            player_name_list.append(player.user_id)
        if error is None:
            response['error_code'] = 0
            data = {
                "player_list": player_name_list,
                "start": start,
                "script_title": script_title        # TODO: change this return
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
        room.update(script_title=script_title)
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
        role_list = models.Role.objects.filter(script_title=script_title)
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
