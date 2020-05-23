from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json

from django.utils.timezone import now
import sys

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
        username = request.POST.get("username", None)
        print(username)
        password = request.POST.get("password", None)
        email = request.POST.get("email", None)
        user = models.User.objects.filter(name=username)
        now_time = now()
        if not user:
            models.User.objects.create(name=username, password=password, email=email,
                                       group_id=2, add_time=now_time, friend_num=0,
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
        friend_list = user.friend_list.split("$$")
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
            friend_list = user.friend_list.split("$$")
            friend_list.append(user_to_be_add_name)
            friend_list2 = user_to_be_add.friend_list.split("$$")
            friend_list2.append(username)
            friend_num1 = user.friend_num + 1
            friend_num2 = user_to_be_add.friend_num + 1
            user.update(friend_list=list2txt(friend_list), friend_num=friend_num1)
            user_to_be_add.update(friend_list=list2txt(friend_list2), friend_num=friend_num2)
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
            friend_list = user.friend_list.split("$$")
            friend_list.remove(user_to_be_delete_name)
            friend_list2 = user_to_be_delete.friend_list.split("$$")
            friend_list2.remove(username)
            friend_num1 = user.friend_num - 1
            friend_num2 = user_to_be_delete.friend_num - 1
            user.update(friend_list=list2txt(friend_list), friend_num=friend_num1)
            user_to_be_delete.update(friend_list=list2txt(friend_list2), friend_num=friend_num2)
        if error is None:
            response['error_num'] = 0
        else:
            response['error_num'] = 1
            response['msg'] = error
    return JsonResponse(response)


def list2txt(friend_list):
    txt = None
    for item in friend_list:
        txt += item
        txt += "$$"
    return txt


def init_room(request):
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        num_person = req['num_person']
        room_name = req['room_name']
        uid = req['user_id']
        room_id = 0
        for i in range(1, 100):
            room = models.game_room.objects.filter(room_ID=i).first()
            if not room:
                room = models.game_room.create(room_ID=i, size=num_person, stage=0, script_title=None)
                room_id = i
                break
        if error is None:
            script = models.script.objects.filter(player_num=num_person)
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
        user=models.game_user.objects.filter(uesr_name=username).first()
        player=models.player.objects.filter(user_id=user.user_id).first()
        player.room_id=room_id
        player.save()
        player_list = models.player.objects.filter(room_id=room_id)
        player_name_list = None
        room = models.game_room.objects.filter(room_id=room_id).first()
        start = False
        script_id = 0
        if room.stage == 1:
            start = True
            script_id = room.script_id
        for player in player_list:
            player_name_list.append(player.user_id)
        if error is None:
            response['error_code'] = 0
            data = {
                "player_list": player_name_list,
                "start": start,
                "script_id": script_id
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
        script_id = req['script_id']
        room = models.game_room.objects.filter(room_id=room_id).first()
        room.script_id = script_id
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
        script_id = req['script_id']
        script=models.script.objects.filter(script_id=script_id).first()
        room=models.game_room.objects.filter(room_id=room_id).first()
        role_list=models.game_role.objects.filter(script_id=script_id)
        truth=script.truth
        murder_id=script.murder_id
        role_id=None
        role_name=None
        background=None
        timeline=None
        task=None
        for role in role_list:
            role_id.append(role.role_id)
            role_name.append(role.role_name)
            background.append(role.background)
            timeline.append(role.timeline)
            task.append(role.task)
        clue_list=models.game_clue.objects.filter(script_id=script_id)
        c_list=None
        clue_id=None
        clue_description=None
        for clue in clue_list:
            c_list.append(clue.text)
            clue_id.append(clue.clue_id)
            clue_description.append(clue.clue_description)
        room.stage=1
        room.script_id=script_id
        room.save()
        if error is None:
            script_tittle = script.title
            data = {
                "script_tittle":script_tittle,
                "role_id":role_id,
                "role_list":role_name,
                "background":background,
                "timeline":timeline,
                "task":task,
                "truth":truth,
                "murder_id":murder_id,
                "clue_id":clue_id,
                "clue_list":c_list,
                "clue_description":clue_description
            }
            response['error_code'] = 0
        else:

            response['error_code'] = 1
            response['msg'] = error
        return JsonResponse(response)


def first_stage(request):
    response = {}
    error = None
    req = json.loads(request.body)
    room_id = req['room_id']
    role_id = req['role_id']
    player_list=models.player.objects.filter(room_id=room_id)
    flag=True
    room=models.game_clue.objects.filter(room_id=room_id).first()
    player_num=room.size
    ready_num=0
    for player in player_list:
        if not player.ready_1:
            if player.role_id == role_id:
                player.ready_1 = True
                player.save()
        else:
            ready_num=ready_num+1
    if error is None:
        data = {
            "player_num":player_num,
            "ready_player_num":ready_num
        }
        response['error_code'] = 0
    else:

        response['error_code'] = 1
        response['msg'] = error
    return JsonResponse(response)


