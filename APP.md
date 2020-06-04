#### 服务器端接口说明

1. ***register***：注册

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
        last_login_time: null
    }
    ```

2. ***login***：登录

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
    
3. ***get_friends_list***：获取好友列表

    ```python
    Input: {
        username: str
    }
    Output['data']: {
        friend_list: str[]
    }
    ```
    
4. ***add_friend_request***：添加好友请求

    ```python
    Input: {
        username: str
        name: str
    }
    ```
    
5. ***delete_friend_request***：删除好友请求

    ```python
    Input: {
        username: str
        name: str
    }
    ```
    
6. ***init_room***：创建房间

    ```python
    Input: {
        username: str
        num_person: int
    }
    Output['data']: {
        room_id: int
        script_to_select: [
            {
                script_id: int
                title: str
                description: str
            }
            ...
        ]
        room_size: int
        player_list: [
            {
                id: int (player_id)
                id_in_room: int
                name: str (username)
            }
            ...
        ]
        master_name: str (or null)
        start: bool
    }
    ```

7. ***upsend_script***：上传自定义剧本

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
                role_name: str
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

8. ***enter_room***：进入房间

    ```python
    Input: {
        username: str
        room_id: int
    }
    Output['data']: {
        room_size: int
        script_id: int (or null)
        player_list: [
            {
                id: int (player_id)
                id_in_room: int
                name: str (username)
            }
            ...
        ]
        master_name: str (or null)
        start: bool
    }
    ```
    
9. ***exit_room***：离开房间

    ```python
    Input: {
        username: str
        room_id: int
    }
    Output['data']: {
        player_list: [
            {
                id: int (player_id)
                id_in_room: int
                name: str (username)
            }
            ...
        ]
        master_name: str (or null)
        start: bool
    }
    ```
    
10. ***room_owner_choose_script***：房主选择剧本

    ```python
    Input: {
        room_id: int
        script_title: str
    }
    ```
    
11. ***start_game***：开始游戏

    ```python
    Input: {
        room_id: int
    }
    Output['data']: {
        script_title: str
        murder: {
            role_id: int
            role_id_in_script: int
            role_name: str
        }
        role_info: [
            {
                player_id: int
                player_id_in_room: int
                name: str (username)
                role_id: int,
                role_id_in_script: int
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
                clue_id_in_script: int
                description: str
            }
            ...
        ]
    }
    ```
    
12. ***check_clue***：玩家查看线索

    ```python
    Input: {
        room_id: int
        role_id: int
        clue_id: int
    }
    Output['data']: {
        clue_owner: {
            player_id: int
            player_id_in_room: int
            role: str (role_name)
        }
        clue_info: {
            text: str
            clue_id: int
            clue_id_in_script: int
            description: str
        }
    }
    ```
    
13. ***refresh_clue***：更新线索发现信息

    ```python
    Input: {
        room_id: int
    }
    Output['data']: [
        {
            clue_id: int
            clue_id_in_script: int
            owner_list: [
                {
                    role_id: int
                    role_id_in_script: int
                    player_id: int
                    player_id_in_room: int
                }
                ...
            ]
            open: int
        }
        ...
    ]
    ```
    
14. ***public_clue***：公开线索

    ```python
    Input: {
        room_id: int
        clue_id: int
    }
    Output['data']: {
        clue_id: int
        clue_id_in_script: int
        text: str
        description: str
    }
    ```
    
15. ***send_message***：聊天

    ```python
    Input: {
        room_id: int
        player_id: int
        message: str
    }
    Output['data']: [
        {
            player_id: int
            player_id_in_room: int
            name: str (username)
            message: str
            send_time: time
        }
        ...
    ]
    ```
    
16. ***synchronize***：玩家游戏状态更新与同步

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

17. ***get_user_room***：获取用户当前所在房间

    ```python
    Input: {
        username: str
    }
    Output['data]: {
        room_id: int (or null)
    }
    ```

18. ***get_room_master***：获取房间房主信息

    ```python
    Input: {
        room_id: int
    }
    Output['data']: {
        id: int (player_id)
        id_in_room: int
        name: str (username)
    }
    ```
