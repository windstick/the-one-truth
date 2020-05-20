<template>
  <div>
    <h1>还没有登陆时显式的页</h1>
  </div>
</template>

<script>
export default {
  name: 'loggedOut',
  components: {
  },
  beforeMount()
  {
    if(this.$parent.User.logIn)
      this.$router.replace('/home/room')
  }
}
</script>

<style>
  h1 {
    text-align: center;
    padding: 20px 0 20px 0;
  }
</style>
