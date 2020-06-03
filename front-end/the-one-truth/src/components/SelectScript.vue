<template>
  <div>
    <h1>选取剧本</h1>
    <h2>
      可供选择的剧本有
    </h2>

    <div id="scripts">
      <div v-for="(script, index) in available_scripts" class="script">
        <input type="radio" :value="index" v-model="chosen_script_index">
        <scriptItem>
          <img src="@/assets/Home/book.png" slot="fig" style="height: 30px;"/>
          <div slot="scriptName">{{script.title}}</div>
          <p slot="intro">{{script.intro}}</p>
        </scriptItem>
      </div>
    </div>

    <el-button @click="chooseScript(chosen_script_index)">确定选取剧本</el-button>
  </div>
</template>

<script>
import scriptItem from './ScriptItem.vue'
export default {
  name: 'selectScript',
  components: {
    scriptItem
  },
  data(){
    return {
      chosen_script_index: 0
    }
  },
  props:
  {
    available_scripts: Array
  },
  methods:{
    chooseScript(i){
      // console.log(i)
      this.$emit('chooseScript', this.available_scripts[i].script_id);
    }
  }
}
</script>

<style>
  h1 {
    text-align: center;
    padding: 20px 0 20px 0;
  }

  .script {
    display: flex;
  }
</style>