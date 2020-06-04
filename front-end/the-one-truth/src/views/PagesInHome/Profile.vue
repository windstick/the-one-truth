<template>
  <div style="text-align:center">
    <h1>个人中心</h1>
    <h2 style="text-align:center;">用户名称：{{User.name}}</h2>
    <h2> 好友列表 </h2>
    <div style="display:flex;flex: 0 0 auto;">
      <FriendTable :friend_list="User.friend_list" style="width: 200px;"/>
    </div>
  </div>
</template>

<script>
import FriendTable from "@/components/FriendTable"
export default {
  name: 'Profile',
  components: {
    FriendTable
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
  }
}
</script>

<style>

</style>