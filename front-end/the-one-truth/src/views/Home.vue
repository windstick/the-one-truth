<template>
  <div id="home">
    <Banner id="banner">
      <div v-show="User.logIn" class="banner_item" @click="roomClick">当前房间</div>
      <div class="banner_item" @click="scriptsClick">剧本</div>
      <div v-if="User.logIn" class="banner_item" @click="profileClick">用户</div>
      <div v-if="!User.logIn" class="banner_item">登录</div>
      <div v-if="!User.logIn" class="banner_item">注册</div>
    </Banner>

    <router-view></router-view>
  </div>
</template>

<script>
// @ is an alias to /src
import Banner from '../components/Banner'

export default {
  name: 'Home',
  components: {
    Banner,
  },
  data(){
    return {
      Room: {
        room_id: 0,
        player_list: [],
        size: 1,
        chosen_script: 0,
        created: 0
      },
      User: {
        logIn: false,
        user_id: 0,
        name: "",
        passwd: ""
      }
    }
  },
  methods: {
    profileClick()
    {
      this.$router.push('/home/profile');
    },
    scriptsClick()
    {
      this.$router.push('/home/scripts');
    },
    roomClick()
    {
      this.$router.push('/home/room');
    }
  }
}
</script>

<style>
  #home{
  }

  .banner_item {
    margin: 0 10px 0 10px;
    padding: 0 10px 0 10px;
    flex: 0 0 auto;
    height: 50px;
    text-align: center;
    line-height: 50px;
  }
</style>
