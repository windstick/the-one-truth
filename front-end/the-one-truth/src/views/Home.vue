<template>
  <div id="home">
    <Banner id="banner">
      <div class="banner_item">剧本</div>
      <div v-show="logIn" class="banner_item">用户</div>
      <div v-show="!logIn" class="banner_item">登录</div>
      <div v-show="!logIn" class="banner_item">注册</div>
    </Banner>
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
    return{
      logIn: false
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