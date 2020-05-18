<template>
  <div class="app">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      count: 0,
      stage: 0,
      dark:[1,0,0,0,0,0],
      light:[0,1,1,1,1,1],
      /* 以下是剧情文本相关的数据 */
      scriptText:0,
      background: '这是背景故事。',
      timeline: '这是时间线。',
      task: '这是任务。',
      truth: '张三是凶手。',

      /* 以下是线索相关的数据 */
      selectedRole:0,
      selectedCriminal:0,
      trueCriminal:0,
      movementPoint:2,
      roles:[
        {id:0,name:'张三'},
        {id:1,name:'李四'},
        {id:2,name:'王五'},
      ],
      clues:[
        {id:0,text:'这是张三的线索,但不会告诉你谁是凶手',show:0},
        {id:1,text:'这是李四的线索，但不会告诉你谁是凶手',show:0},
        {id:2,text:'这是王五的线索，王五看见了张三行凶的过程，可推出张三是凶手',show:0},
      ]

    }
  },
  watch:{
    stage(curval,oldval){
       if(curval==5){
         if(this.selectedCriminal==this.trueCriminal){
           alert('恭喜你找出了凶手,游戏获胜！')
         }
         else{
           alert('没有找对凶手，游戏失败！')
         }
       }
       if(curval==0){
         this.movementPoint=2;
         for(let i=0;i<3;++i){
           this.clues[i].show=0;
         }
       }
    },
  },
  methods:{
    myready:function(){
       this.count=this.count+1;
       if(this.count>0){
         this.count=0;
         this.light[this.stage]=1;
         this.dark[this.stage]=0;
         this.stage=this.stage+1;
         this.light[this.stage]=0;
         this.dark[this.stage]=1;
       }
       if(this.stage==6)this.stage=0;
    },
    searchClue:function(){
      if(this.movementPoint>0 && this.stage==2 && this.clues[this.selectedRole].show==0){
      this.clues[this.selectedRole].show=1;
      this.movementPoint--;
      }
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.el-row {
    margin-bottom: 20px;
    &:last-child {
      margin-bottom: 0;
    }
  }
  .el-col {
    border-radius: 4px;
    text-align: center;
    padding-left: 10px;
    padding-right: 10px;
  }
  .el-col-2{
    border-radius: 4px;
    text-align: center;
    line-height: 300px;
    padding-left: 10px;
    padding-right: 10px;
  }
  .bg-purple-dark {
    background: #99a9bf;
  }
  .bg-purple {
    background: #d3dce6;
  }
  .bg-purple-light {
    background: #e5e9f2;
  }
  .bg-red {
    background: #f56c6c;
  }
  .grid-content {
    border-radius: 4px;
    min-height: 36px;
    line-height: 30px;
  }
  .grid-content2 {
    border-radius: 4px;
    min-height: 36px;
    line-height: 300px;
  }
  .row-bg {
    padding: 10px 0;
    background-color: #f9fafc;
  }
  .el-header, .el-footer {
    background-color: #B3C0D1;
    color: #333;
    text-align: center;
    line-height: 60px;
  }
  
  .el-aside {
    background-color: #D3DCE6;
    color: #333;
    text-align: center;
    line-height: 200px;
  }
  
  .el-main {
    background-color: #E9EEF3;
    color: #333;
    text-align: center;
    line-height: 300px;
  }
  
  body > .el-container {
    margin-bottom: 40px;
  }
  
  .el-container:nth-child(5) .el-aside,
  .el-container:nth-child(6) .el-aside {
    line-height: 260px;
  }
  
  .el-container:nth-child(7) .el-aside {
    line-height: 320px;
  }
</style>
