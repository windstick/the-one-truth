<template>
  <div id="createorjoin">
    <h1>创建或者加入房间</h1>
    <h2>创建房间</h2>
    <label for="createsize">创建房间的大小</label>
      <el-input type="number" id="createsize" v-model.number="roomSize"
        style="margin: 10px 0px;"></el-input>
    <br/>
    <el-button id="create" @click="createRoom">创建房间</el-button>

    <h2>加入房间</h2>
    <label for="roomid">加入房间的编号</label>
      <el-input type="number" id="roomid" v-model.number="roomId"
       style="margin: 10px 0px;"></el-input>
    <br/>
    <el-button id="join" @click="joinRoom">加入房间</el-button>
  </div>
</template>

<script>
export default {
  name: 'createOrJoinRoom',
  components: {
  },
  data() {
    return {
      roomSize: 0,
      roomId: 0
    }
  },
  props: {
    created: Boolean
  },
  methods: {
    createRoom(){
      
      if(Number.isInteger(this.roomSize) && this.roomSize > 0)
      {
        // 这里需要向后端请求的代码，获取roomid（这个任务交给room界面完成吧）
        // console.log(this.roomSize);
        this.$emit('createRoom', this.roomSize)
      }
      else
        alert('Room size has to be a natural number greter than 0!\n')
    },
    joinRoom(){
      if(Number.isInteger(this.roomId) && this.roomId >= 0)
      {
        // 这里需要向后端请求的代码，获取roomid（这个任务交给room界面完成吧）
        console.log(this.roomId);
        this.$emit('joinRoom', this.roomId);
      }
      else
        alert('Room id has to be an Integer');

    }
  }/*,
  watch: {
    created(val, oldVal){
        if(this.created) {
          // console.log('room has been created')
          this.$router.replace('/home/room/selectscript');
        }
    }
  }*/
}
</script>

<style>
  h1 {
    text-align: center;
    padding: 20px 0 20px 0;
  }
</style>