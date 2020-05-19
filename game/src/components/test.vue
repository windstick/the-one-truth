<template>
  <div class="test">
      <p>this is just a test</p>
      <p>{{timeline}}</p>
      <p>{{task}}</p>
      <el-button @click="gogame()"  type="primary">gogame</el-button>
  </div>
</template>

<script>
import Game from '@/components/Game'
export default {
  name:'test',
  data() {
    return {
        timeline:1,
        task:2,
        sc:1,
        pl:1,
    }
  },
  methods:
  {
      gogame:function(){
      this.$router.push({name:'Game',params:{player:this.pl,script_id:this.sc}})
    }
  },
  components: {Game},
  created(){
      console.log(this.$route.params)
      this.timeline=this.$route.params.mytimeline
      this.task=this.$route.params.mytask
  }
}
</script>