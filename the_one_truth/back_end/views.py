from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
import json

from django.utils.timezone import now
import sys

from . import models

# Create your views here.

def index(request):
    return HttpResponse('Hello, world!')


def register_handler(request):
    if request.method == 'POST':
        response = {}
        error = None
        req = json.loads(request.body)
        username = req['username']
        password = req['password']
        email = req['email']
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
        user = models.User.objects.filter(name=username)
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

def check_clue(request):
    print("clue!!")
    if request.method == 'POST':
        response = {}
        error = None

        req = json.loads(request.body)
        room_id = req['room_id']        
        role_id = req['role_id']
        clue_id = req['clue_id']

        # check if clue id is correct
        find_clue = models.game_clue(clue_id = clue_id)
        find_player = models.player.objects.filter(room_id = room_id, role_id= role_id)
        if not find_clue or not find_player:
            error = 'No such clue or no such player'
        else:
            models.player_clue(is_public = False, player_id = find_player.player_id, clue_id = clue_id, room_id = room_id).save()

        if error is None:
            response['error_num'] = 0
        else:
            response['error_num'] = 1
            response['msg'] = error
    return JsonResponse(response)


def refresh_clue(request):
    if request.method == 'POST':
        response = {}
        error = None

        req = json.loads(request.body)
        room_id = req['room_id']        

        # check if clue id is correct
        find_room = models.game_room(room_id = room_id)
        if not find_room:
            error = 'No such room'
        else:
            script_id = models.game_room.objects.filter(room_id = room_id)[0].script_id
            all_clue = models.game_clue.objects.filter(script_id = script_id)
            data = []
            for i in range(len(all_clue)):
                #get player_clue
                clue_id = all_clue[i].clue_id
                player_clue = models.player_clue.objects.filter(clue_id = clue_id, room_id = room_id)[0]
                # if no owner
                if player_clue == None:
                    owner_role_id = None
                    open = False
                else:
                    owner_role_id = player_clue.player_id
                    open = player_clue.is_public
                cur_data = {
                    "clue_id":all_clue[i].clue_id,
                    "owner_role_id":owner_role_id,
                    "open":open
                }
                data.append(cur_data)
            response['data'] = data
        if error is None:
            response['error_num'] = 0
        else:
            response['error_num'] = 1
            response['msg'] = error
    return JsonResponse(response)


def pulic_clue(request):
    if request.method == 'POST':
        response = {}
        error = None

        req = json.loads(request.body)
        room_id = req['room_id']        
        clue_id = req['clue_id']

        # check if clue id is correct
        find_clue = models.game_clue(clue_id = clue_id)
        if not find_clue:
            error = 'No such clue'
        else:
            cur_player_clue = models.player_clue.objects.filter(clue_id = clue_id)[0]
            cur_player_clue.is_public = True
            cur_player_clue.save()

        if error is None:
            response['error_num'] = 0
        else:
            response['error_num'] = 1
            response['msg'] = error
        return JsonResponse(response)
