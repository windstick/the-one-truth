<template>
  <div>
    <h1>Profile page</h1>
    <p>{{User.name}}</p>
  </div>
</template>

<script>
export default {
  name: 'Profile',
  components: {
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