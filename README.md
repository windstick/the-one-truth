## The One Truth 剧本杀平台 (软件工程实习)

#### 服务器端接口说明

1. register：注册

    ```python
    Input: {
        username: str
        password: str
        group_id: int
        email: email
    }
    Output['data']: {
        username: str
        groupid: int
        reg_time: time
        last_login_time: time
    }
    ```

2. login：登录

    ```python
    Input: {
        username: str
        password: str
    }
    Output['data']: {
        username: str
        groupid: int
        last_login_time: time
    }
    ```
    
3. get_friends_list：获取好友列表

    ```python
    Input: {
        username: str
    }
    Output['data']: {
        friend_list: str[]
    }
    ```
    
4. add_friend_request：添加好友请求

    ```python
    Input: {
        username: str
        name: str
    }
    ```
    
5. delete_friend_request：删除好友请求

    ```python
    Input: {
        username: str
        name: str
    }
    ```
    
6. init_room：创建房间

    ```python
    Input: {
        num_person: int
    }
    Output['data']: {
        room_id: int
        script_to_select: str[]
    }
    ```

7. upsend_script

    ```python
    Input: {
        title: str
        truth: str
        description: str
        role_list: [
            {
                name: str
                is_murder: int
                task: str
                background: str
                timeline: str
                role_description: str
            },
            ...
        ]
        clue_list: [
            {
                text: str
                clue_description: str
            },
            ...
        ]
    }
    Output['data']: {
        script_tittle: str,
        player_num: int,
        truth: str,
        description: str,
        murder: int (role id)
    }
    ```

8. enter_room：进入房间

    ```python
    Input: {
        username: str
        room_id: int
        is_master: int
    }
    Output['data']: {
        player_list: [
            {
                id: int (player_id)
                name: str (username)
            }
            ...
        ]
        start: bool
    }
    ```
    
9. exit_room：离开房间

    ```python
    Input: {
        username: str
        room_id: int
        is_master: int
        next_master_name: str (PS: need to give only if is_master == 1)
    }
    Output['data']: {
        player_list: [
            {
                id: int (player_id)
                name: str (username)
            }
            ...
        ]
        start: bool
    }
    ```
    
10. room_owner_choose_script：房主选择剧本

    ```python
    Input: {
        room_id: int
        script_title: str
    }
    ```
    
11. start_game：开始游戏

    ```python
    Input: {
        room_id: int
    }
    Output['data']: {
        script_title: str
        murder_id: int (role_id)
        role_info: [
            {
                player_id: int
                name: str (username)
                role_id: int
                role_name: str
                background: str
                timeline: str
                task: str
                is_murder: int
            }
            ...
        ]
        clue_info: [
            {
                text: str
                clue_id: int
                description: str
            }
            ...
        ]
    }
    ```
    
12. check_clue：玩家查看线索

    ```python
    Input: {
        room_id: int
        role_id: int
        clue_id: int
    }
    Output['data']: {
        clue_owner: {
            player_id: int
            role: str (role_name)
        }
        clue_info: {
            clue_id: int
            text: str
            description: str
        }
    }
    ```
    
13. refresh_clue：更新线索发现信息

    ```python
    Input: {
        room_id: int
    }
    Output['data']: [
        {
            clue_id: int
            owner_list: [
                {
                    role_id: int
                    player_id: int
                }
                ...
            ]
            open: int
        }
        ...
    ]
    ```
    
14. public_clue：公开线索

    ```python
    Input: {
        room_id: int
        clue_id: int
    }
    Output['data']: {
        clue_id: int
        text: str
        description: str
    }
    ```
    
15. send_message：聊天

    ```python
    Input: {
        room_id: int
        player_id: int
        message: str
    }
    Output['data']: [
        {
            player_id: int
            name: str (username)
            message: str
        }
        ...
    ]
    ```
    
16. synchronize：玩家游戏状态更新与同步

    ```python
    Input: {
        room_id: int
        player_id: int
        ready_tag: int
    }
    Output['data']: {
        player_num: int
        ready_player_num: int
        room_stage: {
            before: int
            after: int
        }
    }
    ```
    