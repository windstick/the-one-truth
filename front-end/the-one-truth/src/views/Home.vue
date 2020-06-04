<template>
  <div id="home">
    <Banner id="banner">
      <router-link v-if="User.logIn" to="/home/room">
        <div class="banner_item">
          当前房间
        </div>
      </router-link>

      <router-link to="/home/scripts">
        <div class="banner_item">
          剧本
        </div>
      </router-link>


      <el-dropdown class="banner_item" trigger="click" v-if="User.logIn">
        <div class="avatar-wrapper">
          <div>用户</div>
        </div>
        <el-dropdown-menu slot="dropdown" class="user-dropdown">
          <router-link to="/home/profile">
            <el-dropdown-item>
              个人中心
            </el-dropdown-item>
          </router-link>
          <router-link to="/home/loggedout">
            <el-dropdown-item>
              注销
            </el-dropdown-item>
          </router-link>
        </el-dropdown-menu>
      </el-dropdown>
      <!---router-link v-if="User.logIn" to="/home/profile">
        <div class="banner_item">
          用户
        </div>
      </router-link--->
      
      <router-link v-if="!User.logIn" to="/login">
        <div class="banner_item">登录</div>
      </router-link>

      <router-link v-if="!User.logIn" to="/login">
        <div v-if="!User.logIn" class="banner_item">注册</div>
      </router-link>
    </Banner>

    <keep-alive include="room">
      <router-view :User="User" id="main"></router-view>
    </keep-alive>

    
  </div>
</template>

<script>
// @ is an alias to /src
import Banner from '../components/Banner'

export default {
  name: 'Home',
  components: {
    Banner
  },
  computed: {
      User() {
        // this.$store.dispatch("user/updateFriendListFromNetwork")
        return {
          logIn: this.$store.state.user.login,
          user_id: this.$store.state.user.user_id,
          name: this.$store.state.user.name,
          passwd: this.$store.state.user.passwd,
          friend_list: this.$store.state.user.friend_list
        }
      }
  },
  methods: {
    updateFriendList(){
      this.$store.dispatch("user/updateFriendListFromNetwork")
    }
  }

}
</script>

<style>
  #main{
    padding: 16px;
  }

  .banner_item {
    margin: 0 10px 0 10px;
    padding: 0 10px 0 10px;
    flex: 0 0 auto;
    height: 50px;
    text-align: center;
    line-height: 50px;
  }

  a {
    text-decoration: none;
  }

  a:visited{
    color: rgba(30, 30, 30)
  }

  .router-link-active {
    text-decoration: none;
    background-color: rgba(240, 242, 245);
  }

  .router-link{
    text-decoration: none;
  }


</style>
