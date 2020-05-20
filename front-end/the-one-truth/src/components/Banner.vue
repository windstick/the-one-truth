<template>
  <div id="banner">
    <div id="det_div" @click="iconClick">
      <img src="../assets/Home/detective.png" id="det_img"/>
      <div>The One Truth</div>
    </div>
    
    <slot class="banner_item"></slot>
  </div>
</template>

<script>
export default {
  name: 'Banner',
  components: {
    
  },
  methods: {
    iconClick()
    {
      this.$router.push('/home/loggedout')
    }
  }
}
</script>

<style>
  #banner {
    background-color: white;
    box-shadow: 0 7px 5px rgba(32, 32, 32, 0.3);
    display: flex;
    justify-content: flex-end;
    text-align: center;
  }

  #det_div{
    height: 50px;
    flex: 1 0 auto;
    text-align: left;
    line-height: 50px;
    display: flex;
  }

  #det_img{
    height: 30px;
    margin: 10px 20px 10px 20px;
  }

</style>