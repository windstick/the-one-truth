<template>
  <div>
    <h1>已经成功注销</h1>
  </div>
</template>

<script>
export default {
  name: 'loggedOut',
  components: {
  },
  beforeMount()
  {
    this.$store.commit("user/logOut")
  }
}
</script>

<style>
  h1 {
    text-align: center;
    padding: 20px 0 20px 0;
  }
</style>
