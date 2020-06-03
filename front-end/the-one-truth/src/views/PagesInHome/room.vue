<template>
  <div id="room">
    <div id="tableContainer">
      <el-row :gutter="32">
        <el-col :xs="24" :sm="24" :lg="8">
          <div class="col-wrapper">
            <h1>好友列表</h1>
            <FriendTable :friend_list="User.friend_list"/>
            <el-button @click="updateFriendList" style="margin-top:10px;"> update userlist </el-button>
          </div>

        </el-col>

        <el-col :xs="24" :sm="24" :lg="8">
          <div class="col-wrapper">
          <component :is="currentComponent" :created="roomSession.created"
                      :available_scripts="availableScripts" @createRoom="createRoom"
                      @joinRoom="joinRoom" @chooseScript="chooseScript"> </component>
          </div>
        </el-col>

        <el-col :xs="24" :sm="24" :lg="8">
          <div class="col-wrapper">
            <h1>房间内玩家</h1>
            <p v-show="!roomSession.created">还没有加入房间</p>
            <table v-show="roomSession.created">
              <tr v-for="item in roomSession.player_list">{{item}}</tr>
            </table>
          </div>
        </el-col>
      </el-row>
    </div>

    <div style="text-align: center;">
      <el-button id="enterGame" v-if="ready" @click="enterGame" >进入游戏</el-button>
    </div>
  </div>
</template>


<script>
import CreateOrJoinRoom from "../../components/CreateOrJoinRoom"
import SelectScript from "../../components/SelectScript"
import FriendTable from "../../components/FriendTable"
import {request} from '@/network/request'

export default {
  name: 'room',
  components: {
    SelectScript,
    CreateOrJoinRoom,
    FriendTable
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
          availableScripts: []
        }
  },
  computed: {
    ready(){
      // return true;
      console.log(this.roomSession.choose_script)
      return (this.roomSession.player_list.length === this.roomSession.size) && this.roomSession.choose_script;
    },
    currentComponent(){
      if(this.roomSession.created)
        return "SelectScript"
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
      this.roomSession.size = roomsize;
      this.roomSession.room_id = 102;
      this.roomSession.player_list = ['user0'];
      // 更新房间状态
      this.roomSession.created = true;

      this.availableScripts=[
        {
          img: '@/assets/logo.png',
          title: 'TestScript',
          intro: 'This is a fun script. This is a fun script. This is a fun script. This is a fun script.',
          script_id: 0
        },
        {
          img: '@/assets/logo.png',
          title: 'TestScript2',
          intro: 'This is a fun script. This is a fun script. This is a fun script. This is a fun script.',
          script_id: 1
        }
      ]
      // console.log('room created');
    },
    joinRoom(roomid){
      // console.log('joining room');
      // 向服务器查询特定房间是否存在，存在则继续
      this.roomSession.room_id = 102;
      this.roomSession.player_list = ['user0', 'user1'];
      // 更新房间状态
      this.roomSession.created = true;
      // console.log('room created');
      // console.log(this.roomSession.player_list);
    },
    chooseScript(id){
      this.roomSession.choose_script = true;
      this.roomSession.chosen_script_id = id;
      console.log("ready: " + this.ready)
      // this.ready = true;
    },
    enterGame()
    {
      this.$router.push({
        path: '/game',
        query: {
          script_id: 1,//this.roomSession.chosen_script_id,
          player: 1
        }
      })
    },
    updateFriendList(){
      this.$store.dispatch("user/updateFriendListFromNetwork")
    }
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
