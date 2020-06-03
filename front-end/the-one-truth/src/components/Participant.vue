<template>
  <div>
    <h1>当前房间号为：{{room_id}}</h1>

    <el-button @click="exitRoom">退出房间</el-button>
    <h2>正在等待游戏开始</h2>
  </div>
</template>

<script>
import scriptItem from './ScriptItem.vue'
export default {
  name: 'participant',
  methods: {
    exitRoom(){
      this.$emit('exitRoom');
    }
  },
  props:
  {
    room_id: Number
  }
}
</script>

<style>
  h1 {
    text-align: center;
    padding: 20px 0 20px 0;
  }

  .script {
    display: flex;
  }
</style>