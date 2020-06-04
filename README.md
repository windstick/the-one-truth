# the-one-truth平台说明

The one truth是一款web应用，开发目的是建立一个集成剧本创作和剧本杀游戏的综合平台，该平台需要具有方便易用、稳定可靠的特点，能够让游戏玩家便利地开展剧本杀游戏，也能够让剧本创作与玩家沟通交流，提升剧本质量。



# 部署说明

## 前端部署说明

**安装与运行**

前端采用vue-cli3脚手架框架进行的部署，因此需要系统中安装了node和npm包管理工具，来安装前端页面所依赖的包括Vue组件以及各种插件。具体的下载需要从[官网](https://nodejs.org/en/)下载对应系统版本并且安装。

```shell
# 查看安装状况
node -v
npm -v
```

切换到前端对应的目录，使用npm包管理工具安装相关依赖。

```shell
cd .\front-end\the-one-truth\
npm install
```

等待安装完成后启动，然后根据提示的浏览器端口进行网页访问。

```shell
npm run serve
```



## 后端部署说明

#### 后端运行方式

0. 环境要求

    ```
    python 3.6.8
    Django 3.0.6
    django-cors-headers 3.3.0
    MySQL 8.0.20
    ```

1. 创建数据库

    * 先在MySQL数据库中手动创建数据库：the_one_truth_database

    * 定义数据库 tables

        ```bash
        cd the_one_truth/back_end
        bash init_migration.sh
        ```

    * 批量导入用户数据：生成 sql 文件

        ```bash
        python generate_data.py user load_data.sql
        ```

2. 启动服务器

    ```bash
    cd the_one_truth
    python manage.py runserver 0.0.0.0:8000
    ```

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

# 游戏界面使用说明

## 主界面

在此界面可以完成的功能

- 浏览目前平台所有的剧本简介信息
- 登录
- 注册

![image-20200604232434411](markdown_fig/README.assets/image-20200604232434411.png)



## 房间界面

在此界面可以完成的功能

- 创建一个指定大小的房间
- 加入一个由他人创建的指定编号的房间
- 创建房间者（房主）可以在显示的剧本列表（这些剧本的参与人数和此房间大小相符合）中选取一个剧本
- 刷新当前房间内玩家（手动或自动）
- 进入游戏

![image-20200604232526019](markdown_fig/README.assets/image-20200604232526019.png)



## 游戏界面

此界面可以完成的功能

- 发送和接受消息
- 查看游戏内容，包括背景故事、时间线和人物
- 进行线索的搜证
- 选取凶手
- 查看真相

