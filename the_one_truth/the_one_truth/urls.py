"""the_one_truth URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import back_end.views as bv


urlpatterns = [
    ##=== for testing ===##
    path('admin/', admin.site.urls),
    path('index/', bv.index),
    ##=== user operations ===##
    path('register/', bv.register_handler),
    path('login/', bv.login_handler),
    path('get_friends_list/', bv.get_friend_list_request),
    path('add_friend_request/', bv.add_friend_request),
    path('delete_friend_request/', bv.delete_friend_request),
    ##=== script operations ===##
    path('upsend_script/',bv.upsend_script),
    ##=== room operations ===##
    path('get_room_master/', bv.get_room_master),
    path('get_user_room/', bv.get_user_room),
    path('init_room/',bv.init_room),
    path('enter_room/',bv.enter_room),
    path('exit_room/',bv.exit_room),
    ##=== game operations===##
    path('room_owner_choose_script/',bv.room_owner_choose_script),
    path('start_game/',bv.start_game),
    path('synchronize/', bv.synchronize),
    ##=== clue operations ===##    
    path('check_clue/',bv.check_clue),
    path('refresh_clue/',bv.refresh_clue),
    path('public_clue/',bv.public_clue),
    ##=== dialogue ===##
    path('send_message/', bv.send_msg)
]
