<template>
  <div>
    <div id="tableContainer">
      <div id="tableRow">
        <div id="friendList">
          <h1>好友列表</h1>
          <table>
            <tr v-for="item in User.friend_list">{{item}}</tr>
          </table>
        </div>
        <router-view id="roomCreateBar" :created="roomSession.created" @createRoom="createRoom"
                                                                       @joinRoom="joinRoom"></router-view>
        <div id="playerInRoom"><h1>房间内玩家</h1></div>
      </div>
    </div>
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
          player_list: ['user1', 'user2'],
          size: 1,
          chosen_script: -1,
          created: false,
          user_id: 0
          }
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
      console.log('creating room');
      // 请求房间id（轮询一直到成功为止）
      this.roomSession.room_id = 102;
      // 更新房间状态
      this.roomSession.created = true;
      console.log('room created');
    },
    joinRoom(roomid){
      console.log('joining room');
      // 向服务器查询特定房间是否存在，存在则继续
      this.roomSession.room_id = 102;

      // 更新房间状态
      this.roomSession.created = true;
      console.log('room created');
    }
  }
}

</script>


<style>
  #tableContainer{
    display: table;
  }
  #tableRow{
    display: table-row;
    text-align: center;
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

  #tableRow{
    padding: 10 20 10 20;
  }


</style>
