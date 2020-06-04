<template>
  <div>
    <div id="wrapper">
      <h1>剧本页</h1>
      <div id="tableContainer">
        <el-row :gutter="32" style="align: middle;">
          <el-col :xs="24" :sm="24" :lg="8" id="script_col">
            <div class="col-wrapper">
              <div v-for="(script, index) in scripts" class="script">
                <scriptItem>
                  <img src="@/assets/Home/book.png" slot="fig" style="height: 30px;"/>
                  <div slot="scriptName">{{script.title}}</div>
                  <p slot="intro">{{script.intro}}</p>
                </scriptItem>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>
      <el-button>上传剧本</el-button>
    </div>
  </div>
</template>

<script>
import scriptItem from '@/components/ScriptItem'
export default {
  name: 'Scripts',
  components: {
    scriptItem
  },
  data() {
    return {
      scripts: [
        {
          title: '巴德将军的信',
          intro: '此剧本属于谋杀之谜的入门剧本，游戏时间短，流程简单。新手玩家热身剧本，内容偏简单。'
        },
        {
          title: 'a_test_script_title',
          intro: 'test'
        },
        {
          title: 'a_test_script_title_2',
          intro: 'test2'
        },
        {
          title: 'a_test_script_title_3',
          intro: 'test3'
        }
      ]
    }
  }
}
</script>

<style scope>
  .col-wrapper{

  }
  #wrapper{
    text-align: center
  }
  #script_col{
    margin: 10px auto;
  }
</style>