<template>
  <div>
    <div id="tableContainer">
      <div id="tableRow">
        <div id="friendList">好友列表</div>
        <router-view id="roomCreateBar"></router-view>
        <div id="playerInRoom">房间内玩家</div>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  name: 'room',
  components: {},
}
</script>


<style>
  #tableContainer{
    display: table;
  }
  #tableRow{
    display: table-row;
  }

  #friendList{
    display: table-cell;
    width: 30%;
  }

  #roomCreate{
    display: table-cell;
    width: 30%;
  }

  #playerInRoom{
    display: table-cell;
    width: 30%;
  }


</style>
