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
                                       last_login_time=now_time, friend_list="None")
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
