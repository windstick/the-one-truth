<template>
  <div class="Game">
    <el-container>
  <el-header>THE ONE TRUTH</el-header>
  <el-main>
    <el-row>
  <el-col :span="4"><div v-bind:class="{'grid-content bg-purple-dark':dark[0],'grid-content bg-purple':light[0]}">剧本环节</div></el-col>
  <el-col :span="4"><div v-bind:class="{'grid-content bg-purple-dark':dark[1],'grid-content bg-purple':light[1]}">介绍环节</div></el-col>
  <el-col :span="4"><div v-bind:class="{'grid-content bg-purple-dark':dark[2],'grid-content bg-purple':light[2]}">线索环节</div></el-col>
  <el-col :span="4"><div v-bind:class="{'grid-content bg-purple-dark':dark[3],'grid-content bg-purple':light[3]}">讨论环节</div></el-col>
  <el-col :span="4"><div v-bind:class="{'grid-content bg-purple-dark':dark[4],'grid-content bg-purple':light[4]}">投票环节</div></el-col>
  <el-col :span="4"><div v-bind:class="{'grid-content bg-purple-dark':dark[5],'grid-content bg-purple':light[5]}">真相环节</div></el-col>
</el-row>
<div v-if= "stage==4" class='grid-content bg-red'>
  <el-row>
    请选出你认为的凶手：
    <el-button  v-for= 'role in roles' @click= 'selectedCriminal=role.id'>{{role.name}}</el-button>
  </el-row>
</div>
    <el-row>
      <el-col :span="8">
        <div class='grid-content bg-purple'>
          <el-radio v-model="scriptText" label="0">背景故事</el-radio>
          <el-radio v-model="scriptText" label="1">时间线</el-radio>
          <el-radio v-model="scriptText" label="2">任务</el-radio>
          <el-radio v-model="scriptText" label="3" v-if= 'stage==5'>真相</el-radio>
        </div>
        <div class='grid-content2 bg-purple' v-if= "scriptText==0">{{background}}</div>
        <div class='grid-content2 bg-purple' v-if= "scriptText==1">{{timeline}}</div>
        <div class='grid-content2 bg-purple' v-if= "scriptText==2">{{task}}</div>
        <div class='grid-content2 bg-purple' v-if= "scriptText==3">{{truth}}</div>
      </el-col>
      <el-col :span="8">
        <div v-if= 'stage<=1' class='grid-content bg-purple' >
        </div>
        <div v-if= 'stage>1'> 
        <div class='grid-content bg-purple' >
        <el-radio v-for= 'role in roles' v-model= 'selectedRole' v-bind:label= 'role.id'>{{role.name}}</el-radio>
        <el-button type='info' @click='searchClue()'>搜索| {{movementPoint}}/2</el-button>
        </div>
        <div v-for= 'clue in clues' class='grid-content2 bg-purple' v-if= "clue.id==selectedRole && clue.show==1" >{{clue.text}}</div>        
        </div>
      </el-col>
      <el-col :span="8">
          <div class='grid-content bg-purple' >
             聊天框
            </div>
          <div class='grid-content2 bg-purple' >
             {{chat}}
            </div>
      </el-col>
    </el-row>
<el-footer>
<el-button @click="myready()"  type="primary">准备就绪</el-button>
</el-footer>
</el-main> 
</el-container> 
<el-button @click="gotest()"  type="primary">gotest</el-button>
<p>script_id:{{scriptid}},player:{{player}}</p>
  </div>
</template>

<script>
export default {
  name: 'Game',
  data() {
    return {
      count: 0,
      stage: 0,
      dark:[1,0,0,0,0,0],
      light:[0,1,1,1,1,1],
      /* 以下是剧情文本相关的数据 */
      scriptText:0,
      scriptid:0,
      player:0,
      chat:'聊天内容',
      background: '这是背景故事',
      timeline: '这是时间线。',
      task: '这是任务。',
      truth: '张三是凶手。',

      /* 以下是线索相关的数据 */
      selectedRole:0,
      selectedCriminal:0,
      trueCriminal:0,
      movementPoint:2,
      info:{},
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
    },
    gotest:function(){
      this.$router.push({name:'test',params:{mytimeline:this.timeline,mytask:this.task}})
    }
  },
  mounted () {
    /* this.$axios
      .get('/site/info.json')
      .then(response => (this.task = response))
      .catch(function (error) { // 请求失败处理
        console.log(error);
      });
      */
    this.axios({
        method: 'post',
        url: '/send_message/',
        data:{
        
        //num_person:2
        //group_id:0,
        //is_master:0,
        room_id:1,
        //role_id:0,
        player_id:0,
        message:"msg2"
        //player_id:0,
        //ready_tag:1      
        //username:'user1',
        //script_title:'a_test_script_title'
        //name:"user1"
        //name:'user1'
        //password:'1234567',
        //mail:'5432154321@pku.edu.cn'
        }
      })
      .then(response => (this.task = response.data ,this.background=response.data.name,console.log(response.data)));
      console.log(1)

      
  },
  created(){
      console.log(this.$route.params)
      this.scriptid=this.$route.params.script_id
      this.player=this.$route.params.player
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

