<template>
  <div id="room">
    <div id="tableContainer">
      <div id="tableRow">
        <div id="friendList">
          <h1>好友列表</h1>
          <table>
            <tr v-for="item in User.friend_list">{{item}}</tr>
          </table>
        </div>


        <router-view id="roomCreateBar" :created="roomSession.created" @createRoom="createRoom"
                                                                       @joinRoom="joinRoom"
                                        :available_scripts="availableScripts"
                                                                       @chooseScript="chooseScript"
                                        ></router-view>

        
        <div id="playerInRoom">
          <h1>房间内玩家</h1>
          <p v-show="!roomSession.created">还没有加入房间</p>
          <table v-show="roomSession.created">
            <tr v-for="item in roomSession.player_list">{{item}}</tr>
          </table>
        </div>
      </div>
    </div>

    <button id="enterGame" v-if="ready" @click="enterGame">进入游戏</button>
  </div>
</template>


<script>
export default {
  name: 'room',
  components: {},
  data() {
        return {
          roomSession : {
            room_id: 0,
            player_list: [],
            size: 1,
            choosen_script: false,
            chosen_script_id: -1,
            created: false,
            user_id: 0
          },
          availableScripts: [],
          ready: false
        }
  },
  /*
  computed: {
    ready(){
      return this.roomSession.player_list.length === this.roomSession.size && this.roomSession.choose_script;
    }
  },
  */
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
      console.log('creating room');
      // 请求房间id（轮询一直到成功为止）
      this.roomSession.size = roomsize;
      this.roomSession.room_id = 102;
      this.roomSession.player_list = ['user0'];
      // 更新房间状态
      this.roomSession.created = true;

      this.availableScripts=[
        {
          img: '../assets/logo.png',
          title: 'TestScript',
          intro: 'This is a fun script. This is a fun script. This is a fun script. This is a fun script.',
          script_id: 0
        },
        {
          img: '../assets/logo.png',
          title: 'TestScript2',
          intro: 'This is a fun script. This is a fun script. This is a fun script. This is a fun script.',
          script_id: 1
        }
      ]
      console.log('room created');
    },
    joinRoom(roomid){
      console.log('joining room');
      // 向服务器查询特定房间是否存在，存在则继续
      this.roomSession.room_id = 102;
      this.roomSession.player_list = ['user0', 'user1'];
      // 更新房间状态
      this.roomSession.created = true;
      console.log('room created');
      console.log(this.roomSession.player_list);
    },
    chooseScript(id){
      this.roomSession.choose_script = true;
      this.roomSession.chosen_script_id = id;
      console.log("ready: " + this.ready)
      this.ready = true;
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
    }
  }
}

</script>


<style>
  #tableContainer{
    display: table;
    margin: 50px 0;
  }
  #tableRow{
    display: table-row;
    text-align: center;
    background-color: white;
  }

  #friendList{
    display: table-cell;
    width: 500px;
  }

  #roomCreateBar{
    display: table-cell;
    width: 500px;
  }

  #playerInRoom{
    display: table-cell;
    width: 500px;
  }

  #room{
    text-align: center;
  }

</style>
