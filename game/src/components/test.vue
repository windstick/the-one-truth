<template>
  <div class="test">
      <p>this is just a test</p>
      <p>{{message}}</p>
  </div>
</template>

<script>
import Game from '@/components/Game'
export default {
  name:'test',
  data() {
    return {
        message:1
    }
  },
  components: {Game},
  created(){
      console.log(this.$route.params)
      this.message=this.$route.params.mytimeline
  }
}
</script>