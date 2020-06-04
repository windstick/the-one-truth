<template>
  <div id="room">
    <div id="tableContainer">
      <el-row :gutter="32">
        <el-col :xs="24" :sm="24" :lg="8">
          <div class="col-wrapper">
            <h1>好友列表</h1>
            <FriendTable :friend_list="User.friend_list"/>
            <el-button @click="updateFriendList" style="margin-top:10px;"> 更新好友列表 </el-button>
          </div>

        </el-col>

        <el-col :xs="24" :sm="24" :lg="8">
          <div class="col-wrapper">
          <component :is="currentComponent" :created="roomSession.created"
                      :available_scripts="availableScripts" 
                      :room_id="roomSession.room_id"
                      @joinRoom="joinRoom" @chooseScript="chooseScript"
                      @createRoom="createRoom" @exitRoom="exitRoom"> </component>
          </div>
        </el-col>

        <el-col :xs="24" :sm="24" :lg="8">
          <div class="col-wrapper">
            <h1>房间内玩家</h1>
            <p v-show="!roomSession.created">还没有加入房间</p>
            <!---table v-show="roomSession.created">
              <tr v-for="item in roomSession.player_list">{{item}}</tr>
            </table--->
            <el-table :data="roomSession.player_list" style="width: 100%; padding-top: 15px;">
              <el-table-column label="用户id" min-width="100" prop="id"/>
              <el-table-column label="玩家身份" min-width="100" prop="id_in_room"/>
              <el-table-column label="用户名称" min-width="100" prop="name"/>
            </el-table>
            <el-button @click="updatePlayerList" style="margin-top:10px;"> 更新玩家列表 </el-button>
          </div>
        </el-col>
      </el-row>
    </div>

    <div style="text-align: center;">
      <el-button id="enterGame" v-if="ready" type="primary" @click="enterGame" >进入游戏</el-button>
    </div>
  </div>
</template>


<script>
import CreateOrJoinRoom from "../../components/CreateOrJoinRoom"
import SelectScript from "../../components/SelectScript"
import FriendTable from "../../components/FriendTable"
import Participant from "../../components/Participant"
import {request} from '@/network/request'

export default {
  name: 'room',
  components: {
    SelectScript,
    CreateOrJoinRoom,
    FriendTable,
    Participant
  },
  data() {
        return {
          roomSession : {
            room_id: 0,
            player_list: [],
            size: 1,
            choose_script: false,
            chosen_script_id: -1,
            created: false,
            user_id: 0
          },
          availableScripts: [],
          player_id: 0,
          is_master: false
        }
  },
  computed: {
    ready(){
      // return true;
      // console.log(this.roomSession.size)
      return (this.roomSession.player_list.length === this.roomSession.size) && this.roomSession.choose_script;
    },
    currentComponent(){
      if(this.roomSession.created)
        if(this.ismaster)
          return "SelectScript"
        else
          return "Participant"
      else return "CreateOrJoinRoom"
    }
  },
  props: {
    User: {
      type: Object,
      default(){
        return {
          logIn: true,
          user_id: 0,
          name: "",
          passwd: "",
          friend_list: []
        }
      }
    }
  },
  methods: {
    createRoom(roomsize){
      // console.log('creating room');
      // 请求房间id（轮询一直到成功为止）
      request({
        method: 'post',
        url: '/api/init_room/',
        data: {
          num_person: roomsize,
          username: this.User.name
        }
      }).then(msg =>{
        if(msg.error_code != 0) console.log(msg)
        console.log(msg)
        this.player_id = 0
        this.roomSession.size = roomsize
        this.roomSession.room_id = msg.data.room_id
        this.roomSession.player_list = [{id: this.User.id, id_in_room: 0, name: this.User.name}]
        this.ismaster = true
        this.availableScripts = msg.data.script_to_select.map(function(n){
          return {
            img: '@/assets/logo.png',
            title: n.title,
            intro: n.description,
            script_id: 0
          }
        })
        // 更新房间状态
        this.roomSession.created = true;
      }).catch(err =>{
        console.log(err)
      })
      console.log(this.roomSession);
    },
    joinRoom(roomid){
      request({
        method: 'post',
        url: '/api/enter_room/',
        data: {
          username: this.User.name,
          room_id: roomid
        }
      }).then(msg => {
        console.log(msg)
        if(msg.error_code != 0) 
        {
          alert(msg.msg)
        }
        else{
          this.roomSession.room_id = roomid
          this.roomSession.size = msg.data.room_size
          this.roomSession.created = true;
          this.roomSession.player_list = msg.data.player_list
          this.roomSession.roomsize = msg.data.room_size
          this.ismaster = (msg.data.master_name == this.User.name)
          // 判断是否选取了剧本
          this.roomSession.choose_script = (msg.data.script_id != null)
          this.roomSession.chosen_script_id = msg.data.script_id
          // console.log("ismaster: " + this.ismaster)

          // 取player_id
          for(let i = 0; i < msg.data.player_list.length; ++i)
          {
            if(msg.data.player_list[i].name == this.User.name)
            {
              this.player_id = msg.data.player_list[i].id_in_room
              break
            }
          }
          console.log("playerid: " + this.player_id)
        }
        
      }).catch(err =>{
        console.log(err)
        alert('room doesn\'t exist')
      })
    },
    exitRoom(){
      request({
        method: 'post',
        url: '/api/exit_room/',
        data: {
          username: this.User.name,
          room_id: this.roomSession.room_id
        }
      }).then(msg => {
        // this.$router.push({path:'/home/room'})
        alert("exit success")
      })
    },
    chooseScript(id){
      request({
        method: 'post',
        url: '/api/room_owner_choose_script/',
        data: {
          room_id: this.roomSession.room_id,
          script_title: this.availableScripts[id].title
        }
      }).then(msg=>{
        alert('choose script ' + this.availableScripts[id].title)
      }).catch(err=>{
        console.log(err)
      })

      this.roomSession.choose_script = true;
      this.roomSession.chosen_script_id = id;
      // console.log("ready: " + this.ready)
      // this.ready = true;
    },
    enterGame()
    {
      this.$router.push({
        path: '/game',
        query: {
          script_id: 0, // 目前后端不会用到，需要记录一下
          player: this.player_id,
          room_id: this.roomSession.room_id
        }
      })
    },
    updateFriendList(){
      this.$store.dispatch("user/updateFriendListFromNetwork")
    },
    updatePlayerList(){
      request({
        method: 'post',
        url: '/api/enter_room/',
        data: {
          username: this.User.name,
          room_id: this.roomSession.room_id
        }
      }).then(msg => {
        // console.log(msg)
        if(msg.error_code != 0) 
        {
          alert(msg.msg)
        }
        else{
          this.roomSession.player_list = msg.data.player_list
          console.log(msg.data)
          this.roomSession.choose_script = (msg.data.script_id != null)
          this.roomSession.chosen_script_id = msg.data.script_id

          // 取player_id
          for(let i = 0; i < msg.data.player_list.length; ++i)
          {
            if(msg.data.player_list[i].name == this.User.name)
            {
              this.player_id = msg.data.player_list[i].id_in_room
              break
            }
          }
          console.log("playerid: " + this.player_id)
        }
      }).catch(err =>{
        console.log(err)
        alert('room doesn\'t exist')
      })
    }
  },
  created(){
    // console.log(this.User.name)
    // 判断当前用户是否已经在一个房间中，如果已经在一个房间中，显示对应房间的界面，需要手动退出
    request({
        method: 'post',
        url: '/api/get_user_room/',
        data: {
          username: this.User.name
        }
      }).then(msg => {
        // 判断是否在房间内
        // console.log(this.User.name)
        if(msg.data.room_id != null)
        {
          this.joinRoom(msg.data.room_id)
        }
        // 如果在房间内，判断是否是master
      })
  }
}

</script>


<style>
  .col-wrapper{
    background: #fff;
    padding: 5px 16px 16px 16px;
    margin-bottom: 32px;
    border: 1px solid #e1e2e5;
    text-align: center;
    border-radius: 8px;
  }
</style>
